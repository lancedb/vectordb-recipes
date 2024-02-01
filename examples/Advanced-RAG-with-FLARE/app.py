from langchain import PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceBgeEmbeddings
from io import BytesIO
from langchain.document_loaders import PyPDFLoader
import gradio as gr
import lancedb
from langchain.vectorstores import LanceDB
from langchain.document_loaders import ArxivLoader
from langchain.chains import FlareChain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from langchain.llms import OpenAI
import getpass

os.environ["OPENAI_API_KEY"] = "sk-yourapikeyforopenai"

llm = OpenAI()

model_name = "BAAI/bge-large-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

# here is example https://arxiv.org/pdf/2305.06983.pdf
# you need to pass this number to query 2305.06983
# fetch docs from arxiv, in this case it's the FLARE paper
docs = ArxivLoader(query="2305.06983", load_max_docs=2).load()

# instantiate text splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)

# split the document into chunks
doc_chunks = text_splitter.split_documents(docs)

# lancedb vectordb
db = lancedb.connect("/tmp/lancedb")
table = db.create_table(
    "documentsai",
    data=[
        {
            "vector": embeddings.embed_query("Hello World"),
            "text": "Hello World",
            "id": "1",
        }
    ],
    mode="overwrite",
)
vector_store = LanceDB.from_documents(doc_chunks, embeddings, connection=table)

vector_store_retriever = vector_store.as_retriever()

flare = FlareChain.from_llm(
    llm=llm, retriever=vector_store_retriever, max_generation_len=300, min_prob=0.45
)


# Define a function to generate FLARE output based on user input
def generate_flare_output(input_text):
    output = flare.run(input_text)
    return output


input = gr.Text(
    label="Prompt",
    show_label=False,
    max_lines=1,
    placeholder="Enter your prompt",
    container=False,
)

iface = gr.Interface(
    fn=generate_flare_output,
    inputs=input,
    outputs="text",
    title="My AI bot",
    description="FLARE implementation with lancedb & bge embedding.",
)

iface.launch(debug=True, share=True)
