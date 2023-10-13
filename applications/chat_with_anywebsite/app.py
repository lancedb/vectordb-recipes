import os
import re
import openai
import gradio as gr
from typing import List, Union
import lancedb
import langchain
from langchain.vectorstores import LanceDB
from langchain.chains import RetrievalQA
from langchain.llms import CTransformers
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.document_loaders import WebBaseLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders.csv_loader import CSVLoader

# Set OpenAI API key as an environment variable
#os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
#OPENAI_API_KEY  ='YOURTKEYpaste her-sk-9Tnu7YtoZNNqs

def find_urls(text: str) -> List:

    # Regular expression to match common URLs and ones starting with 'www.'
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.findall(text)

# for pdf reading
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def website_loader(website: Union[str, list[str]]) -> List[langchain.schema.document.Document]:

    print("Loading website(s) into Documents...")
    documents = WebBaseLoader(web_path=website).load()
    print("Done loading website(s).")
    return documents


def split_text(documents: List) -> List[langchain.schema.document.Document]:

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=120,
                                                   chunk_overlap=20,
                                                   length_function=len
                                                   )
    chunks = text_splitter.transform_documents(documents)
    print("Done splitting documents.")
    return chunks



def bge_embedding(chunks:List):

    print("Creating bge embedder...")
    
    model_name = "BAAI/bge-base-en"
    encode_kwargs = {'normalize_embeddings': True} # set True to compute cosine similarity

    embedder = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={'device': 'cpu'},
        encode_kwargs=encode_kwargs
    )

    return embedder


def create_vector_store(chunks: List[langchain.schema.document.Document],
                        embedder):
  
    print("Creating vectorstore...")
    #vectorstore = FAISS.from_documents(chunks, embedder)
    #return vectorstore

    db = lancedb.connect('/tmp/lancedb')
    table = db.create_table("pdf_sear1ch", data=[
        {"vector": embedder.embed_query("Hello World"), "text": "Hello World", "id": "1"}
    ], mode="overwrite")
    vectorstore = LanceDB.from_documents(chunks, embedder, connection=table)
    return vectorstore

# download llm  model & put in working directory
# https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

def load_llm():
    # Load the locally downloaded model here
    llm = CTransformers(
        model = "mistral-7b-instruct-v0.1.Q5_K_M.gguf",    
        model_type="mistral"
    )
    return llm



def create_retriever(vectorstore) :

    print("Creating vectorstore retriever...")
    retriever = vectorstore.as_retriever()
    return retriever


def embed_user_query(query: str) -> List[float]:

    core_embeddings_model = bge_embedding(chunks)  # bge ranked top on leaderbord  https://huggingface.co/spaces/mteb/leaderboard
    #HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
    #                                model_kwargs={'device':"cpu"})
    
    #OpenAIEmbeddings() 
    embedded_query = core_embeddings_model.embed_query(query)
    return embedded_query

def similarity_search(vectorstore: langchain.vectorstores,
                      embedded_query: List[float]) -> List[langchain.schema.document.Document]:

    response = vectorstore.similarity_search_by_vector(embedded_query, k=4)
    return response


def create_chatbot(retriever):

    #llm = ChatOpenAI(model="gpt-3.5-turbo")
    llm = load_llm()
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
        )

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory
        )
    return conversation_chain

def chat(conversation_chain, input: str) -> str:

    return conversation_chain.run(input)

text = """
your expert at answering the quetions which asked by user. I need you to go to the following URLs and get information about them 
https://blog.lancedb.com/llms-rag-the-missing-storage-layer-for-ai-28ded35fa984
and this https://blog.lancedb.com/context-aware-chatbot-using-llama-2-lancedb-as-vector-database-4d771d95c755

if you dont know the answer said that 'i dont know this dude'
"""


# This chatbot_instance will be initialized once a URL is provided.
chatbot_instance = None

def respond(message, chat_history):
    global chatbot_instance
    if message.lower() == "clear":
        chatbot_instance = None  # Reset the chatbot instance
        chat_history.clear()  # Clear chat history
        return "", chat_history

    urls = find_urls(message)

    # If the chatbot is not yet initialized and we have URLs, initialize it
    if not chatbot_instance and urls:
        #documents = load_pdf(path)
        documents = website_loader(urls)
        chunks = split_text(documents)
        embedder = bge_embedding(chunks)
        vectorstore = create_vector_store(chunks, embedder)
        retriever = create_retriever(vectorstore)
        chatbot_instance = create_chatbot(retriever)
        bot_message = "Chatbot initialized ! Now how can I help you?"
    else:
        if chatbot_instance:
            bot_message = chat(chatbot_instance, message)
        else:
            bot_message = "Please provide a URL to initialize the chatbot first, then ask any questions related to that site."

    chat_history.append((message, bot_message))
    return "", chat_history

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    user_query = gr.Textbox(label="Your Query", placeholder="How can I assist you today?")
    clear = gr.ClearButton([user_query, chatbot])

    user_query.submit(respond, [user_query, chatbot], [user_query, chatbot])

demo.launch(debug=True)
