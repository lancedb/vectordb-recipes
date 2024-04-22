import os
import torch
import lancedb
from dotenv import load_dotenv
from langchain_community.vectorstores import LanceDB
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from lancedb.embeddings import get_registry
from lancedb.pydantic import Vector, LanceModel
from lancedb.rerankers import ColbertReranker

load_dotenv()

class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata if metadata is not None else {}

    def __repr__(self):
        return f"Document(page_content='{self.page_content}', metadata={self.metadata})"


def get_rag_output(question):
    input_pdf_file = "https://d18rn0p25nwr6d.cloudfront.net/CIK-0001559720/8a9ebed0-815a-469a-87eb-1767d21d8cec.pdf"

    # Create your PDF loader
    loader = PyPDFLoader(input_pdf_file)

    # Load the PDF document
    documents = loader.load()

    # Chunk the pdf data 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    openai = get_registry().get("openai").create()

    class Schema(LanceModel):
        text: str = openai.SourceField()
        vector: Vector(openai.ndims()) = openai.VectorField()

    embedding_function = OpenAIEmbeddings()

    db = lancedb.connect("~/langchain")
    table = db.create_table(
        "pdf_data",
        schema=Schema,
        mode="overwrite",
    )

    # Load the document into LanceDB
    db = LanceDB.from_documents(docs, embedding_function, connection=table)
    table.create_fts_index("text", replace=True)

    reranker = ColbertReranker()
    docs_n = (
        table.search(question, query_type="hybrid")
        .limit(5)
        .rerank(reranker=reranker)
        .to_pandas()["text"]
        .to_list()
    )

    metadata = {"source": input_pdf_file}
    docs_with_metadata = [
        Document(page_content=text, metadata=metadata) for text in docs_n
    ]

    vectorstore = LanceDB.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"]),
    )

    retriever = vectorstore.as_retriever()

    print("retriver", retriever)

    rag_prompt_template = """
    As an AI Assistant, your role is to provide authentic and accurate responses. Analyze the question and its context thoroughly to determine the most appropriate answer.

    **Instructions:**
    - Understand the context and nuances of the question to identify relevant and precise information.
    - if its general greeting then  answer should be  hellow how can i help you,please ask related quetions so i can help
    - If an answer cannot be conclusively determined from the provided information, inform the user rather than making up an answer.
    - When multiple interpretations of a question exist, briefly present these viewpoints, then provide the most plausible answer based on the context.
    - Focus on providing concise and factual responses, excluding irrelevant details.
    - For sensitive or potentially harmful topics, advise users to seek professional advice or consult authoritative sources.
    - Keep your answer clear and within 500 words.

    **Context:**
    {context}

    **Question:**
    {question}

    """

    prompt = PromptTemplate(
        template=rag_prompt_template,
        input_variables=[
            "context",
            "question",
        ],
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    output = rag_chain.invoke(question)
    return output
