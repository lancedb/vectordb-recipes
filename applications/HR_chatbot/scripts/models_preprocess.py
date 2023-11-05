
from langchain.vectorstores import LanceDB
import lancedb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import  ChatOpenAI
from langchain.chains import RetrievalQA
# load agents and tools modules
import pandas as pd
from io import StringIO
from langchain.tools.python.tool import PythonAstREPLTool
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain import LLMMathChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from scripts.load_llm import llm_openai


class HRChatbot:
    def __init__(self, df_path, text_data_path, user):
        self.df_path = df_path
        self.text_data_path = text_data_path
        self.user = user
        self.llm = llm_openai().llm
        self.df = None
        self.timekeeping_policy = None
        self.agent = None

        self.load_data()
        self.initialize_tools()
      

    def load_data(self):
        # Load text documents
        loader = TextLoader(self.text_data_path)
        docs = loader.load()

        # Split documents into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=30,
        )
        documents = text_splitter.split_documents(docs)

        # Create Hugging Face embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            model_kwargs={'device': 'cpu'}
        )

        # create lancedb vectordb
        db = lancedb.connect('/tmp/lancedb')
        table = db.create_table("pandas_docs", data=[
            {"vector": embeddings.embed_query("Hello World"), "text": "Hello World", "id": "1"}
        ], mode="overwrite")
        self.vectorstore = LanceDB.from_documents(documents, embeddings, connection=table)

        self.df = pd.read_csv(self.df_path)

    def initialize_tools(self):
        # Initialize retrieval question-answering model
        # Initialize tools for the agent
        timekeeping_policy = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(),
        )
        python = PythonAstREPLTool(locals={"df": self.df})
        calculator = LLMMathChain.from_llm(llm=self.llm, verbose=True)

        # Set up variables and descriptions for the tools
        user = self.user
        df_columns = self.df.columns.to_list()
        tools = [
            Tool(
                name = "Timekeeping Policies",
                func=timekeeping_policy.run,
                description="""
                Useful for when you need to answer questions about employee timekeeping policies.

                <user>: What is the policy on unused vacation leave?
                <assistant>: I need to check the timekeeping policies to answer this question.
                <assistant>: Action: Timekeeping Policies
                <assistant>: Action Input: Vacation Leave Policy - Unused Leave
                ...
                """
            ),
            Tool(
                name = "Employee Data",
                func=python.run,
                description = f"""
                Useful for when you need to answer questions about employee data stored in pandas dataframe 'df'. 
                Run python pandas operations on 'df' to help you get the right answer.
                'df' has the following columns: {df_columns}
                
                <user>: How many Sick Leave do I have left?
                <assistant>: df[df['name'] == '{user}']['vacation_leave']
                <assistant>: You have n  vacation_leave left.              
                """
            ),
            Tool(
                name = "Calculator",
                func=calculator.run,
                description = f"""
                Useful when you need to do math operations or arithmetic operations.
                """
            ),

        ]


        # Initialize the LLM agent
        agent_kwargs = {'prefix': f'You are friendly HR assistant. You are tasked to assist the current user: {user} on questions related to HR. ...'}
        self.timekeeping_policy = timekeeping_policy
        self.agent = initialize_agent(tools, self.llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, agent_kwargs=agent_kwargs)

    def get_response(self, user_input):
        response = self.agent.run(user_input)
        return response
