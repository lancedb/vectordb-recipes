## URL Scrapping RAG

### Overview
This repository contains code and implementation for URL Scrapping RAG. 
The main feature of this repo is it scraps the input URL but that's not the end of it. This builds different it goes to the depths of URL can say nested and then scraps those URLs as well. After chunking of data, uses Lance DB as vector database to store and retrieve documents related to queries via Sentence Transformers Embeddings. It uses open source llama-3.1 for generating outputs deployed on Groq. You can feed any URL to it and asks related questions.

### Examples
Question | What is CUDA ? |
--- | --- 
RAG Retrieval | CUDA stands for Compute Unified Device Architecture. It is a development environment created by NVIDIA for creating high-performance applications that can run on NVIDIA GPUs. The CUDA Toolkit provides a set of tools, libraries, and programming models for developers to build and optimize applications that can take advantage of the massively parallel processing capabilities of NVIDIA GPUs.

### CODE
Colab Demo for the RAG Fusion <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/URL-Scrapping-RAG/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
