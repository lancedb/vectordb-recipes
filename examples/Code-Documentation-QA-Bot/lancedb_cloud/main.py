# %% [markdown]
# # Code documentation Q&A bot example with LangChain
#
# This Q&A bot will allow you to query your own documentation easily using questions. We'll also demonstrate the use of LangChain and LanceDB using the OpenAI API.
#
# In this example we'll use Pandas 2.0 documentation, but, this could be replaced for your own docs as well

import argparse
import os
import pickle
import re
import zipfile
from pathlib import Path

import openai
import requests
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import BSHTMLLoader
from langchain_community.vectorstores import LanceDB
from langchain_openai import OpenAI, OpenAIEmbeddings


def get_document_title(document_list):
    titles = []
    for doc in document_list:
        if "metadata" in doc and "source" in doc["metadata"]:
            m = str(doc["metadata"]["source"])
            title = re.findall("numpy_docs(.*).html", m)
            if title:
                titles.append(title[0])
            else:
                titles.append("")
        else:
            titles.append("")
    return titles


def arg_parse():
    default_query = "tell me about the numpy library?"
    # default_query = "What's the current version of numpy?"

    parser = argparse.ArgumentParser(description="Code Documentation QA Bot")
    parser.add_argument(
        "--query", type=str, default=default_query, help="query to search"
    )
    parser.add_argument("--openai-key", type=str, help="OpenAI API Key")
    args = parser.parse_args()

    if not args.openai_key:
        if "OPENAI_API_KEY" not in os.environ:
            raise ValueError(
                "OPENAI_API_KEY environment variable not set. Please set it or pass --openai_key"
            )
    else:
        openai.api_key = args.openai_key

    return args


def pre_process():
    from tqdm import tqdm

    docs = []
    docs_path = Path("docs.pkl")
    for p in tqdm(Path("numpy_docs").rglob("*.html")):
        if p.is_dir():
            continue
        # loader = UnstructuredHTMLLoader(p)
        loader = BSHTMLLoader(p, open_encoding="utf8")
        raw_document = loader.load()
        # docs.append(raw_document)
        title = get_document_title(raw_document)
        m = {"title": title}
        if raw_document:
            raw_document[0].metadata.update(m)
            raw_document[0].metadata["source"] = str(raw_document[0].metadata["source"])
            docs.extend(raw_document)

    if docs:
        with open(docs_path, "wb") as fh:
            pickle.dump(docs, fh)
    else:
        with open(docs_path, "rb") as fh:
            docs = pickle.load(fh)

    return docs


if __name__ == "__main__":
    args = arg_parse()

    numpy_docs = requests.get("https://numpy.org/doc/1.26/numpy-html.zip")
    with open("numpy-html.zip", "wb") as f:
        f.write(numpy_docs.content)

    file = zipfile.ZipFile("numpy-html.zip")
    file = file.extractall(path="numpy_docs")

    docs = pre_process()

    print("Loaded {} documents".format(len(docs)))
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()

    db_url = "db://your-project-slug"
    api_key = "sk_..."
    region = "us-east-1"
    table_name = "langchain_vectorstore"

    vectorstore = LanceDB(
        embedding=embeddings,
        uri=db_url,  # your remote database URI
        api_key=api_key,
        region="us-east-1",
        table_name=table_name,  # Optional, defaults to "vectors"
        mode="overwrite",  # Optional, defaults to "overwrite"
    )

    # insert documents in batches
    batch_size = 10000
    for i in range(0, len(documents), batch_size):
        print(f"ingesting batch of {i} : {i+batch_size}")
        batch = documents[i : i + batch_size]
        vectorstore.add_documents(batch)

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=vectorstore.as_retriever()
    )

    result = qa.run(args.query)
    print(result)
