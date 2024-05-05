import os
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from langchain import hub
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import LanceDB
from langchain.document_loaders import PyPDFLoader
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_cohere import CohereRerank
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.llms import LlamaCpp


# Environment variables for sensitive information
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")

app = FastAPI(title="Medical Information Retrieval API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


# Load the document
DATA_PATH = "data/"


loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

docs = loader.load()
logging.info("Document loader done.")

# Set up the text processing and model chain
#llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

# download weights from https://huggingface.co/PrunaAI/OpenBioLLM-Llama3-8B-GGUF-smashed/tree/main
llm = LlamaCpp(
    model_path="/content/OpenBioLLM-Llama3-8B.Q4_K_S.gguf",  # path of gguf weight
    temperature=0.75,
    n_ctx=2048,
    verbose=False,  # Verbose is required to pass to the callback manager
)

embeddings_med = SentenceTransformerEmbeddings(model_name="NeuML/pubmedbert-base-embeddings")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

logging.info("Embedding and LLM setup done.")

splits = text_splitter.split_documents(docs)
vectorstore = LanceDB.from_documents(documents=splits, embedding=embeddings_med)
retriever = vectorstore.as_retriever()
logging.info("Retriever setup done.")

compressor = CohereRerank(cohere_api_key=COHERE_API_KEY)
compression_retriever = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=retriever)
logging.info("Cohere compression retriever setup done.")

chain = RetrievalQA.from_chain_type(llm=llm, retriever=compression_retriever)
logging.info("Chain ready for query processing.")

chain = RetrievalQA.from_chain_type(llm=llm, retriever=compression_retriever)


class QueryRequest(BaseModel):
    query: str

@app.post("/query/", response_model=dict)
async def handle_query(request: QueryRequest):
    try:
        compressed_docs = compression_retriever.invoke(request.query)
        # Assuming pretty_print_docs function returns a string
        response = chain({"query": request.query})
        print("response",response['result'])
        return {"answer": response['result']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

