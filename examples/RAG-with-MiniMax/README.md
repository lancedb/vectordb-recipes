# RAG with MiniMax and LanceDB

This example demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline using [MiniMax](https://www.minimaxi.com/) as the LLM provider and [LanceDB](https://lancedb.com/) as the vector database.

## Overview

- **Web Scraping**: Scrapes web pages and extracts text content.
- **Chunking & Embeddings**: Splits text into chunks and generates embeddings using `sentence-transformers`.
- **Vector Storage**: Stores document embeddings in LanceDB for efficient similarity search.
- **RAG Query**: Retrieves the most relevant document chunks and sends them to MiniMax M2.7 (via OpenAI-compatible API) to generate answers.

## MiniMax API

[MiniMax](https://www.minimaxi.com/) provides an OpenAI-compatible API endpoint, making it easy to integrate with existing OpenAI SDK workflows.

- **Base URL**: `https://api.minimax.io/v1`
- **Models**: `MiniMax-M2.7` (latest, 1M context), `MiniMax-M2.7-highspeed`

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set your MiniMax API key:
   ```bash
   export MINIMAX_API_KEY="your-api-key-here"
   ```

3. Run the script:
   ```bash
   python main.py
   ```

   Or open the notebook in Google Colab:

   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/RAG-with-MiniMax/RAG_with_MiniMax.ipynb)
