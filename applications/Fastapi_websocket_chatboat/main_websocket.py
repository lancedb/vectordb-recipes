import os
import lancedb
import shutil
import uvicorn
import openai
from fastapi import FastAPI, HTTPException, WebSocket, UploadFile, File
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import LanceDB
from langchain.text_splitter import RecursiveCharacterTextSplitter
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel


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
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    
    {context}
    Question: {question}
    Helpful Answer:"""

    OPENAI_API_KEY = "sk-yourkey"

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


# WebSocket endpoint for chat interaction
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                agent = (
                    setup_chain()
                )  # Setup agent for each request to use the latest uploaded file
                response = agent.run(data)
                await websocket.send_text(response)
            except Exception as e:
                await websocket.send_text(f"Error: {str(e)}")
    except Exception as e:
        await websocket.close(code=1001, reason=str(e))


# Endpoint for chatbot interaction
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    agent = setup_chain()
    response = agent.run(request.prompt)
    return {"response": response}


# Health check endpoint
@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Chatbot API is running!"}


# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
