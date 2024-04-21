import os
import torch
from lancedb import connect
from lancedb.pydantic import Vector, LanceModel
from lancedb.embeddings import get_registry
from lancedb.rerankers import ColbertReranker
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import LanceDB

# Set environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-default-key")

class Document:
    """Class to represent a document with content and metadata."""
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Document(page_content='{self.page_content}', metadata={self.metadata})"

def get_rag_output(question):
    """Process a PDF and return outputs based on the RAG and TTS methodology."""
    input_pdf_file = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001559720/8a9ebed0-815a-469a-87eb-1767d21d8cec.pdf"

    # Load PDF document
    loader = PyPDFLoader(input_pdf_file)
    documents = loader.load()

    # Split the document into manageable texts
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    # Embedding and Database Setup
    openai = get_registry().get("openai").create()
    class Schema(LanceModel):
        text: str = openai.SourceField()
        vector: Vector(openai.ndims()) = openai.VectorField()

    db = connect("~/langchain")
    table = db.create_table("airbnb", schema=Schema, mode="overwrite")
    db = LanceDB.from_documents(docs, OpenAIEmbeddings(), connection=table)
    table.create_fts_index("text", replace=True)

    # Rerank search results
    reranker = ColbertReranker()
    reranker_docs = table.search(question, query_type="hybrid").limit(5).rerank(reranker=reranker).to_pandas()["text"].to_list()
    docs_with_metadata = [Document(page_content=text, metadata={'source': input_pdf_file}) for text in reranker_docs]

    return docs_with_metadata

