import openai
import uvicorn
import lancedb
from fastapi import FastAPI, Request, Form
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
import openai
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import LanceDB
from langchain.chat_models import ChatOpenAI

app = FastAPI()
# Set your OpenAI API key here
OPENAI_API_KEY = "sk-"

def setup_chain():
    # Define file path and template
    filepath= "Food_and_Nutrition.pdf"

    template = """Use the following pieces of context to answer the question at the end.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.
    Use three sentences maximum and keep the answer as concise as possible.
    Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:"""

    # Initialize embeddings, loader, and prompt
    embeddings = OpenAIEmbeddings(openai_api_key="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")
   # loader = CSVLoader(file_path=file, encoding='utf-8')
    loader = PyPDFLoader(filepath)
    # docs = loader.load()
    docs = loader.load_and_split()
    prompt = PromptTemplate(input_variables=["context", "question"], template=template)

    
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

    db = LanceDB.from_documents(docs, embeddings, connection=table)
    retriever = db.as_retriever()
    chain_type_kwargs = {"prompt": prompt}

    # Initialize ChatOpenAI
    llm =  ChatOpenAI(openai_api_key="sk-")
  
    # Setup RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        verbose=True
    )
    return chain
  
agent = setup_chain()

@app.get("/")
def read_root(request: Request):
    return {"message": "Welcome to the health food  Chatbot API!"}

@app.post("/prompt")
def process_prompt(prompt: str = Form(...)):
    response = agent.run(prompt)
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
