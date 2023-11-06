from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import  ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import  ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import openai
import os

load_dotenv()
class llm_openai:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key= os.environ["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo",
            temperature=0.0,
        )

# you can use any open source models also
# you need to download model in your local system & kept it in script directory then use
# def load_llm():
#     # Load the locally downloaded model here
#     llm = CTransformers(
#         model = "mistral-7b-instruct-v0.1.Q4_K_S.gguf",    
#         model_type="mistral"
#     )
#     return llm

#check below code & replace it with openai with any models
# pip install CTransformers
#pip install langchain


#     self.llm = CTransformers(
#         model = "mistral-7b-instruct-v0.1.Q4_K_S.gguf",    
#         model_type="mistral"
#     )
