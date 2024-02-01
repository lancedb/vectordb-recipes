import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import openai
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import LanceDB
from langchain.text_splitter import RecursiveCharacterTextSplitter
import lancedb
import shutil
import os

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Chatbot RAG API",
    description="This is a chatbot API template for RAG system.",
    version="1.0.0",
)


# Pydantic model for chatbot request and response
class ChatRequest(BaseModel):
    prompt: str


class ChatResponse(BaseModel):
    response: str


# Global variable to store the path of the uploaded file
uploaded_file_path = None


# Endpoint to upload PDF
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global uploaded_file_path
    uploaded_file_path = f"uploaded_files/{file.filename}"
    os.makedirs(os.path.dirname(uploaded_file_path), exist_ok=True)
    with open(uploaded_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}


# Setup LangChain
def setup_chain():
    global uploaded_file_path
    if not uploaded_file_path or not os.path.exists(uploaded_file_path):
        raise HTTPException(
            status_code=400, detail="No PDF file uploaded or file not found."
        )

    template = """Use the following pieces of context to answer the question at the end.
    Given the context from the uploaded document, provide a concise and
    accurate answer to the question. The document contains detailed and 
    specific information, so the answer should directly reflect the content of the document.
    If the answer is not known, or if the document does not contain the information, state that the answer is not available in the document.
    
    {context}
    Question: {question}
    Helpful Answer:"""

    OPENAI_API_KEY = "sk-yorapikey"

    loader = PyPDFLoader(uploaded_file_path)
    docs = loader.load_and_split()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=50)
    documents = text_splitter.split_documents(docs)

    prompt = PromptTemplate(input_variables=["context", "question"], template=template)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    db_lance = lancedb.connect("/tmp/lancedb")
    table = db_lance.create_table(
        "my_table",
        data=[
            {
                "vector": embeddings.embed_query("Hello World"),
                "text": "Hello World",
                "id": "1",
            }
        ],
        mode="overwrite",
    )

    db = LanceDB.from_documents(documents, embeddings, connection=table)
    retriever = db.as_retriever()
    chain_type_kwargs = {"prompt": prompt}

    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        verbose=True,
    )
    return chain


# Endpoint for chatbot interaction
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    agent = (
        setup_chain()
    )  # Setup agent for each request to use the latest uploaded file
    response = agent.run(request.prompt)
    return {"response": response}


# Health check endpoint
@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Chatbot API is running!"}


# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
