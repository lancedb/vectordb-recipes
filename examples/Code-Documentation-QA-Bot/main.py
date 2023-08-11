# %% [markdown]
# # Code documentation Q&A bot example with LangChain
#
# This Q&A bot will allow you to query your own documentation easily using questions. We'll also demonstrate the use of LangChain and LanceDB using the OpenAI API.
#
# In this example we'll use Pandas 2.0 documentation, but, this could be replaced for your own docs as well

import os
import openai
import argparse
import lancedb
import re
import pickle
import requests
import zipfile
from pathlib import Path

from langchain.document_loaders import BSHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import LanceDB
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def get_document_title(document):
    m = str(document.metadata["source"])
    title = re.findall("pandas.documentation(.*).html", m)
    if title[0] is not None:
        return(title[0])
    return ''

def arg_parse():
    default_query = "What are the major differences in pandas 2.0?"

    parser = argparse.ArgumentParser(description='Code Documentation QA Bot')
    parser.add_argument('--query', type=str, default=default_query, help='query to search')
    parser.add_argument('--openai-key', type=str, help='OpenAI API Key')
    args = parser.parse_args()

    if not args.openai_key:
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError("OPENAI_API_KEY environment variable not set. Please set it or pass --openai_key")
    else:
        openai.api_key = args.openai_key

    return args

if __name__ == "__main__":
    args = arg_parse()

    docs_path = Path("docs.pkl")
    docs = []

    pandas_docs = requests.get("https://eto-public.s3.us-west-2.amazonaws.com/datasets/pandas_docs/pandas.documentation.zip")
    with open('/tmp/pandas.documentation.zip', 'wb') as f:
        f.write(pandas_docs.content)

    file = zipfile.ZipFile("/tmp/pandas.documentation.zip")
    file.extractall(path="/tmp/pandas_docs")

    if not docs_path.exists():
        for p in Path("/tmp/pandas_docs/pandas.documentation").rglob("*.html"):
            print(p)
            if p.is_dir():
                continue
            loader = BSHTMLLoader(p, open_encoding="utf8")
            raw_document = loader.load()

            m = {}
            m["title"] = get_document_title(raw_document[0])
            m["version"] = "2.0rc0"
            raw_document[0].metadata = raw_document[0].metadata | m
            raw_document[0].metadata["source"] = str(raw_document[0].metadata["source"])
            docs = docs + raw_document

        with docs_path.open("wb") as fh:
            pickle.dump(docs, fh)
    else:
        with docs_path.open("rb") as fh:
            docs = pickle.load(fh)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()

    db = lancedb.connect('/tmp/lancedb')
    table = db.create_table("pandas_docs", data=[
        {"vector": embeddings.embed_query("Hello World"), "text": "Hello World", "id": "1"}
    ], mode="overwrite")
    docsearch = LanceDB.from_documents(documents, embeddings, connection=table)

    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

    result = qa.run(args.query)
    print(result)
