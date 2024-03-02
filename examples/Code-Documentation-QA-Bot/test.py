import pytest
import os
import argparse
import lancedb
import pickle
import requests
import zipfile
from pathlib import Path
from main import get_document_title

from langchain.document_loaders import BSHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# TESTING ===============================================================


@pytest.fixture
def mock_embed(monkeypatch):
    def mock_embed_query(query, x):
        return [0.5, 0.5]

    monkeypatch.setattr(OpenAIEmbeddings, "embed_query", mock_embed_query)


def test_main(mock_embed):
    os.mkdir("./tmp")
    args = argparse.Namespace(query="test", openai_key="test")
    os.environ["OPENAI_API_KEY"] = "test"

    docs_path = Path("docs.pkl")
    docs = []

    pandas_docs = requests.get(
        "https://eto-public.s3.us-west-2.amazonaws.com/datasets/pandas_docs/pandas.documentation.zip"
    )
    with open("./tmp/pandas.documentation.zip", "wb") as f:
        f.write(pandas_docs.content)

    file = zipfile.ZipFile("./tmp/pandas.documentation.zip")
    file.extractall(path="./tmp/pandas_docs")

    if not docs_path.exists():
        for p in Path("./tmp/pandas_docs/pandas.documentation").rglob("*.html"):
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

    db = lancedb.connect("./tmp/lancedb")
    table = db.create_table(
        "pandas_docs",
        data=[
            {
                "vector": OpenAIEmbeddings().embed_query("Hello World"),
                "text": "Hello World",
                "id": "1",
            }
        ],
        mode="overwrite",
    )
    # docsearch = LanceDB.from_documents(documents, OpenAIEmbeddings, connection=table)

    # qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever())

    # result = qa.run(args.query)
    # print(result)
