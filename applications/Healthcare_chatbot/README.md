## Overview
This project introduces a healthcare-related Retrieval-Augmented Generation (RAG) chatbot, designed to deliver quick  responses to medical inquiries. Utilizing  OpenBioLLM-Llama3 / openai llm and the NeuML's PubMedBERT for embedding,
this chatbot is adept at processing and responding to medical data queries.

![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/6027ccb2-0917-45e4-97f4-6739aa420082)


## Key Features
### Language Model: 
For demo purpose  here we are using openeai llm model.
but you can try OpenBioLLM-Llama3 or medical-specific llm model.

To utilize OpenBioLLM-Llama3 .download model in the local system & pass the path of it 
link for downloading ggmf version moedl https://huggingface.co/PrunaAI/OpenBioLLM-Llama3-8B-GGUF-smashed

use below code for replacing it with openai llm
```
from langchain_community.llms import LlamaCpp

llm = LlamaCpp(
    model_path="/content/OpenBioLLM-Llama3-8B.Q2_K.gguf",
    temperature=0.75,
    n_ctx=2048,
    top_p=1,
    verbose=True,  # Verbose is required to pass to the callback manager
)
```



### Embeddings: 
Uses NeuML's PubMedBERT (https://huggingface.co/NeuML/pubmedbert-base-embeddings), which is fine-tuned on PubMed data with the BERT architecture to ensure high relevance and contextual accuracy in responses.

### Database and Framework: 
Incorporates the LanceDB vector database and Cohere reranker within the LangChain framework to enhance efficient query processing and response generation.

## Installation
Follow these steps to set up the chatbot on your local machine:

Clone the repository & install 

```pip install -r requirements.txt```

## Start the application:
```
uvicorn main:app --reload
```


After launching the server, open the ```index.html ```
file in any web browser to start interacting with the chatbot.


## Usage

Use the chatbot via the provided web interface. Enter your medical-related questions into the chat input box, and receive responses generated from the integrated language models and databases.



## Note
Please be advised that while the chatbot provides information based on learned data, it can occasionally deliver incorrect information or miss critical nuances. Always consult with a healthcare professional before making any medical decisions based on advice received from the chatbot.

## Disclaimer
This chatbot is intended for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition
