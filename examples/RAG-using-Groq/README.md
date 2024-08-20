## URL Scrapping RAG

### Overview
This repository contains code and implementation for URL Scrapping RAG.  
Below are the mentioned step wise explanation :-  
Step 1 - Using the given URL, scrap the data and find all the existing URLs.  
Step 2 - Create a graph of base url along with it's scrapped sub URLs with the given depth.  
Step 3 - Traverse through the graph and store URL along with it's scrapped data in json format.  
Step 4 - Convert the data into chunks and store embeddings along with chunks in Vector DB.  
Step 5 - Retrieve the most 5 relevant documents related to query from DB.  
Step 6 - Send the query along with documents to llama 3.1 deployed on Groq.  
Step 7 - The returned output is the answer to your query.  

### Examples
Question | What is CUDA ? |
--- | --- 
RAG Retrieval | CUDA stands for Compute Unified Device Architecture. It is a development environment created by NVIDIA for creating high-performance applications that can run on NVIDIA GPUs. The CUDA Toolkit provides a set of tools, libraries, and programming models for developers to build and optimize applications that can take advantage of the massively parallel processing capabilities of NVIDIA GPUs.

### CODE
Colab Demo for the RAG Fusion <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/URL-Scrapping-RAG/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
