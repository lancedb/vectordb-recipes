# Multilingual-RAG

![Multilingual-RAG](https://github.com/akashAD98/Multilingual-RAG/assets/62583018/a84e1839-a311-496c-b545-3533ef348dea.png)

## Overview
Multilingual-RAG is an innovative question-answering system with multilingual capabilities, capable of understanding and generating responses in multiple languages. It is built upon the powerful architecture of Large Language Models (LLMs) with Retrieve-And-Generate (RAG) capabilities. This application harnesses the capabilities of Cohere's multilingual embeddings, LanceDB vector store, LangChain for question answering, and Argos Translate for seamless translation between languages. The user interface is provided by Gradio, ensuring a smooth and interactive user experience.

## Supported Languages
Multilingual RAG is designed to support over 100 languages. The specific list of supported languages depends on the capabilities of the Cohere multilingual model and Argos Translate. By default, it includes support for English, Hindi, French, and Turkish languages. Additional languages can be added to suit your use case.

## Getting Started
Follow these instructions to set up Multilingual-RAG in your local environment.

### Prerequisites
Ensure you have the following prerequisites installed:
- Python 3.x

Create a `.env` file and add your Cohere API key:
just rename `.env-example` with `.env` & past your API



## Installation
You can install the required dependencies using the following commands:

```
pip install -r requirements.txt
```
For Argos Translate, you can install it as follows:

```
git clone https://github.com/argosopentech/argos-translate.git
cd argos-translate
virtualenv env
source env/bin/activate
pip install -e .
```

## Running the App
To run the Multilingual-RAG app, use the following command:
Currently, support text/pdf file - change the file path inside main.py

```
python3 main.py
```
