#import libraries
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



class ChatbotHelper:

    def __init__(self):
        self.chatbot_instance = None
        self.chat_history = []
        self.chunks = None

    def find_urls(self, text: str) -> List[str]:
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.findall(text)

    def initialize_chatbot(self, urls: List[str]):
        documents = self.load_website_content(urls)
        chunks = self.split_text(documents)
        embedder = self.bge_embedding(chunks)
        vectorstore = self.create_vector_store(chunks, embedder)
        retriever = self.create_retriever(vectorstore)
        self.chatbot_instance = self.create_chatbot(retriever)
        return "Chatbot initialized! How can I assist you? now ask your Quetions" 

    def load_website_content(self, urls):
        print("Loading website(s) into Documents...")
        documents = WebBaseLoader(web_path=urls).load()
        print("Done loading website(s).")
        return documents

    def load_llm(self):
        # download your llm in system or use it else
        #llm = CTransformers(
        #    model="mistral-7b-instruct-v0.1.Q5_K_M.gguf",
        #    model_type="mistral"
        )
        llm = CTransformers(model='TheBloke/Mistral-7B-v0.1-GGUF', model_file='mistral-7b-v0.1.Q4_K_M.gguf',model_type="mistral")
        return llm 

    def split_text(self, documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=120,
            chunk_overlap=20,
            length_function=len
        )
        chunks = text_splitter.transform_documents(documents)
        print("Done splitting documents.")
        return chunks

    def bge_embedding(self, chunks):
        print("Creating bge embedder...")
        model_name = "BAAI/bge-base-en"
        encode_kwargs = {'normalize_embeddings': True}
        embedder = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs=encode_kwargs
        )
        return embedder

    def create_vector_store(self, chunks, embedder):
        print("Creating vectorstore...")
        db = lancedb.connect('/tmp/lancedb')
        table = db.create_table("pdf_search", data=[
            {"vector": embedder.embed_query("Hello World"), "text": "Hello World", "id": "1"}
        ], mode="overwrite")
        vectorstore = LanceDB.from_documents(chunks, embedder, connection=table)
        return vectorstore

    def create_retriever(self, vectorstore):
        print("Creating vectorstore retriever...")
        retriever = vectorstore.as_retriever()
        return retriever

    def embed_user_query(self, query):
        if self.chunks is None:
            return "Chatbot not initialized. Please provide a URL first."
        core_embeddings_model = self.bge_embedding(self.chunks)
        embedded_query = core_embeddings_model.embed_query(query)
        return embedded_query

    def create_chatbot(self, retriever):
        llm = self.load_llm()
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

    def chat(self, conversation_chain, input):
        return conversation_chain.run(input)

    def respond(self, message):
        if message.lower() == "clear":
            self.chatbot_instance = None
            self.chat_history.clear()
            return "", self.chat_history

        urls = self.find_urls(message)

        if not self.chatbot_instance and urls:
            bot_message = self.initialize_chatbot(urls)
        else:
            if self.chatbot_instance:
                bot_message = self.chat(self.chatbot_instance, message)
            else:
                bot_message = "Please provide a URL to initialize the chatbot first, then ask any questions related to that site."

        self.chat_history.append((message, bot_message))
        chat_history_text = "\n".join([f"User: {msg[0]}\nBot: {msg[1]}\n" for msg in self.chat_history])
        return bot_message

    def run_interface(self):

 
        iface = gr.Interface(
            fn=self.respond,
            title="Chatbot with URL or any website ",
            inputs=gr.Textbox(label="Your Query", placeholder="Type your query here...",lines=5),
            outputs=[gr.Textbox(label="Chatbot Response", type="text", default="Chatbot response will appear here.", lines=10)],
    
        )
        iface.launch()

if __name__ == "__main__":
    chatbot_helper = ChatbotHelper()
    chatbot_helper.run_interface()
