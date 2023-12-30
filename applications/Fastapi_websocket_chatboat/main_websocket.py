import uvicorn
import lancedb
from fastapi import FastAPI, WebSocket, Form
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import LanceDB

app = FastAPI()

# Setup function for the chatbot agent
def setup_chain():
    template = """Use the following pieces of context to answer the question at the end...
                  {context}
                  Question: {question}
                  Helpful Answer:"""

    filepath = "Food_and_Nutrition.pdf"
    
    embeddings = OpenAIEmbeddings(openai_api_key="sk-")
    loader = PyPDFLoader(filepath)
    docs = loader.load_and_split()
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)

    #lancedb as vectordb
    db_lance = lancedb.connect("/tmp/lancedb")
    table = db_lance.create_table(
        "my_table",
        data=[{"vector": embeddings.embed_query("Hello World"), "text": "Hello World", "id": "1"}],
        mode="overwrite",
    )

    db = LanceDB.from_documents(docs, embeddings, connection=table)
    retriever = db.as_retriever()
    chain_type_kwargs = {"prompt": prompt}

    llm = ChatOpenAI(openai_api_key="sk-")

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        verbose=False
    )
    return chain

agent = setup_chain()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the health food Chatbot API!"}

# WebSocket endpoint    # Create DocArrayInMemorySearch and retriever
    # db = DocArrayInMemorySearch.from_documents(docs, embeddings)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            print("websocket started")
            # Receive the prompt
            prompt = await websocket.receive_text()
            
            # Process the prompt using your existing logic
            response = agent.run(prompt)
            
            # Send the response back
            await websocket.send_text(response)
    except Exception as e:
        # Handle exceptions or disconnections
        print(f"Error: {e}")
        await websocket.close()

# POST endpoint for processing prompts
@app.post("/prompt")
def process_prompt(prompt: str = Form(...)):
    response = agent.run(prompt)
    return {"response": response}

# Main function to run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
