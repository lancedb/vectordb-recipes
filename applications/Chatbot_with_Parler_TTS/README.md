# Chat with PDF using LanceDB and Paler TTS
This application integrates a PDF chat functionality using LanceDB with advanced RAG (Retrieval-Augmented Generation) methods and
leverages the Paler Text-to-Speech (TTS) model for audio output.

It is designed to enable high-quality text and speech interaction with PDF documents.
![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/a4446072-8d8a-4048-a78d-a6030cc20bae)

## Features

Hybrid Search: Combines vector-based and keyword searches to improve result relevance. 

Full-Text Search (FTS): Utilizes Tavity for enhanced text search capabilities within documents.

Colbert Reranker: Improves the accuracy of search results by reranking them based on relevance.

Langchain Prompts: Controls LLM (Large Language Model) outputs using customized prompts for more tailored interactions.

Paler Text-to-Speech (TTS): A lightweight, high-quality TTS model that mimics various speech styles and attributes.

## Installation
Clone the repository and install the required packages:
```
pip install -r requirements.txt
```

## Running the Application
Start the application by running the main script. This will launch a Gradio interface accessible via a web browser:

create  ```.env ``` file & pass the openai_api_key. or simply rename the ```.env-example ``` file to ```.env``` 

```
python3 main.py  # Gradio app will run
```
## Outputs
The application provides two types of outputs from the processed PDF documents:

Text: Extracted and processed text displayed in a user-friendly format.
Audio: Natural sounding speech generated from the text, customizable by speaker characteristics such as gender and pitch.

