"""
Chatbot for talking to Podcast using Langchain, Ollama and LanceDB
"""

from langchain.document_loaders import WikipediaLoader
import pandas as pd
from langchain.memory import ConversationSummaryMemory
import lancedb
from langchain.vectorstores import LanceDB
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain


def lanceDBConnection(embed):
    db = lancedb.connect("/tmp/lancedb")
    table = db.create_table(
        "pdf_search",
        data=[{"vector": embed.embed_query("Hello World"), "text": "Hello World"}],
        mode="overwrite",
    )
    return table


def vectorStoreSetup(query, OPENAI_KEY):
    docs = WikipediaLoader(query=query, load_max_docs=2).load()
    # chunking
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(docs)
    # OpenAI embeddings
    embed = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    # LanceDB as vector store
    table = lanceDBConnection(embed)
    vectorstore = LanceDB.from_documents(
        documents=all_splits,
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_KEY),
        connection=table,
    )
    return vectorstore


def retrieverSetup(text, OPENAI_KEY):
    vectorstore = vectorStoreSetup(text, OPENAI_KEY)
    # define ChatOllama: by default takes llama2-4bit quantized model
    llm = ChatOllama()
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )
    retriever = vectorstore.as_retriever()
    # define Retrieval Chain for retriver
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    return qa


def chat(qa, question):
    # chat query
    r = qa.run({"question": question})
    return r
