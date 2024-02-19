"""
Chatbot for talking to Github Codespaces using Langchain, Qwen and LanceDB
"""

import os
import shutil
import lancedb

from langchain.memory import ConversationSummaryMemory
from langchain_community.document_loaders import GitLoader
from langchain.vectorstores import LanceDB
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain


def lanceDBConnection(embed):
    db = lancedb.connect("/tmp/lancedb")
    table = db.create_table(
        "github_repo",
        data=[{"vector": embed.embed_query("Hello World"), "text": "Hello World"}],
        mode="overwrite",
    )

    return table


def vectorStoreSetup(query_path):
    temp_repo_dir = "./example_data/test_repo1/"
    if os.path.exists(temp_repo_dir):
        shutil.rmtree(temp_repo_dir)
    docs = GitLoader(
        clone_url=query_path,
        repo_path=temp_repo_dir,
        file_filter=lambda file_path: file_path.endswith(".py")
        or file_path.endswith(".md")
        or file_path.endswith(".js"),
    )
    docs = docs.load()

    # chunking
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    all_splits = text_splitter.split_documents(docs)

    # Huggingface embeddings
    embed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # LanceDB as vector store
    table = lanceDBConnection(embed)
    vectorstore = LanceDB.from_documents(
        documents=all_splits,
        embedding=HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        ),
        connection=table,
    )

    return vectorstore


def retrieverSetup(text):
    vectorstore = vectorStoreSetup(text)
    # define ChatOllama: using Qwen model for LLM
    llm = ChatOllama(model="qwen")
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
