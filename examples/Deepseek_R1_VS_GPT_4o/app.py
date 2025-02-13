from lancedb.rerankers import LinearCombinationReranker
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import LanceDB
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from langchain.memory import ConversationBufferMemory

#Pass opeani key or use any LLM
import os
os.environ["OPENAI_API_KEY"] = ""

class QueryProcessor:
    def __init__(self, file_path, db_url="lancedb_temp", table_name="lancedb_indic"):
        """
        Initialize the QueryProcessor with the PDF file and set up the vector store.

        Parameters:
            file_path (str): Path to the PDF file.
            db_url (str): URI for the LanceDB vector store.
            table_name (str): Name of the table in LanceDB.
        """
        # Load and process the PDF document
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        text_splitter = CharacterTextSplitter()
        self.documents = text_splitter.split_documents(documents)

        # Initialize embeddings and vector store

        #deepseek-r1:1.5b embeddings
        embeddings = OllamaEmbeddings(model="deepseek-r1:1.5b")
        
        # Add reranker
        self.reranker = LinearCombinationReranker(weight=0.3)
        self.docsearch = LanceDB.from_documents(
            self.documents, embeddings, reranker=self.reranker
        )

        print("Embedding stored in lancedb")

        #deepseek-r1:1.5b llm 
        self.llm = OllamaLLM(
                model="deepseek-r1:1.5b",
                streaming=True
                )
      
        self.memory = ConversationBufferMemory(memory_key="chat_history")

    def generate_prompt_template(self, main_instructions, prompt_instructions, context_name, query):
        """
        Generate a prompt template for LangChain LLM.

        Parameters:
            main_instructions (str): Main instructions for the LLM.
            prompt_instructions (str): Additional instructions for how to use the data.
            context_name (str): The name of the context (e.g., search results).
            query (str): The query from the user.

        Returns:
            PromptTemplate: The generated prompt template.
        """
        template = f"""{main_instructions}

        {prompt_instructions}

        {context_name}:
        {{context}}

        Previous Conversations:
        {{chat_history}}
        Human: {query}
        Chatbot:"""
        return PromptTemplate(template=template, input_variables=["context", "chat_history"])

    def get_answer(self, query):
        """
        Process a query and return the answer based on the preloaded PDF.

        Parameters:
            query (str): The user's query.

        Returns:
            str: The answer to the query.
        """
        # Perform similarity search
        docs = self.docsearch.similarity_search_with_relevance_scores(query)

        # Generate a prompt
        prompt = self.generate_prompt_template(
            main_instructions="Act as a knowledgeable assistant. Answer the query comprehensively and concisely based on the provided content.",
            prompt_instructions=(
                "Focus on extracting the most relevant and accurate information from the context. "
                "Prioritize clarity, conciseness, and detail in your response. "
                "When summarizing, ensure key points are highlighted without losing important nuances. "
                "If the context is insufficient to fully address the query, acknowledge the limitation clearly."
            ),
            context_name="PDF Content",
            query=query,
        )

        # Create the LangChain pipeline
        chain = prompt | self.llm | StrOutputParser()

        # Invoke the chain and get the answer
        answer = chain.invoke({"context": docs, "chat_history": self.memory})
        return answer

# Initialize the QueryProcessor with the PDF file (done once)
file_path = "Dolat_Capital_Zomato_Initiating_Coverage.pdf"
query_processor = QueryProcessor(file_path)

print("Query Processor initialized")
answer = query_processor.get_answer(query)
print("Answer:", answer)
