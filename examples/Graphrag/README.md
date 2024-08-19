# GraphRAG: Enhancing Retrieval-Augmented Generation with Knowledge Graphs

This repository contains the implementation and experiments for [GraphRAG](https://github.com/microsoft/graphrag) , an advanced version of Retrieval-Augmented Generation (RAG) that 
uses knowledge graphs to improve the retrieval and generation process for complex queries.

## Overview
GraphRAG builds upon traditional RAG by constructing a hierarchical knowledge graph from raw text, allowing it to extract deeper insights and make more accurate connections between entities and relationships. This method is ideal for handling large-scale knowledge bases and dynamic datasets, where complex reasoning is required.

Both GraphRAG and traditional RAG have their strengths, and this repository offers tools to help you experiment with both methods and optimize them for your specific needs.

## Features

-Graph Construction: Build a structured knowledge graph from text data for more efficient retrieval.
-Enhanced Query Processing: Utilize global and local search modes to extract relevant data.
-LLM Integration: Integrate retrieved data into large language models to generate accurate and contextually relevant responses.
-Optimizations: Suggestions for reducing costs using a local LLaMA model for GraphRAG or applying optimization techniques for traditional RAG.


## Learn More: Blog

For a detailed explanation of GraphRAG check out our blog post:

[Read the Blog Post](https://blog.lancedb.com/p/4107b81a-8acf-49fe-9bd0-8781d1291fad/)


## Experimentation and Source Code

To explore and run experiments with both GraphRAG and traditional RAG, access the source code and experiment setup in the provided Colab notebook:

Run Experiments in Google Colab

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/graphrag/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>



