# langchain Chatbot

from langchain.document_loaders import DataFrameLoader
import pandas as pd
from langchain.memory import ConversationSummaryMemory
import lancedb
from langchain.vectorstores import LanceDB
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain


def lanceDBConnection(dataset):
    db = lancedb.connect("/tmp/lancedb")
    table = db.create_table("tb", data=dataset, mode="overwrite")
    return table


def vectorStoreSetup(text, OPENAI_KEY):
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
    emb = embedding.embed_query(text)
    dataset = [{"vector": emb, "text": text}]

    table = lanceDBConnection(dataset)

    df = pd.DataFrame(dataset)
    loader = DataFrameLoader(df)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = LanceDB.from_documents(
        documents=all_splits,
        embedding=OpenAIEmbeddings(openai_api_key=OPENAI_KEY),
        connection=table,
    )
    return vectorstore


def retrieverSetup(text, OPENAI_KEY):
    vectorstore = vectorStoreSetup(text, OPENAI_KEY)
    llm = ChatOpenAI(openai_api_key=OPENAI_KEY)
    memory = ConversationSummaryMemory(
        llm=llm, memory_key="chat_history", return_messages=True
    )

    retriever = vectorstore.as_retriever()
    qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)
    return qa


def chat(qa, question):
    r = qa(question + "?")
    return r["answer"]
