# RAG with MiniMax and LanceDB

This example demonstrates how to build a Retrieval-Augmented Generation (RAG) pipeline using [MiniMax](https://www.minimaxi.com/) as the LLM provider and [LanceDB](https://lancedb.com/) as the vector database.

## Overview

- **Web Scraping**: Scrapes web pages and extracts text content.
- **Chunking & Embeddings**: Splits text into chunks and generates embeddings using `sentence-transformers`.
- **Vector Storage**: Stores document embeddings in LanceDB for efficient similarity search.
- **RAG Query**: Retrieves the most relevant document chunks and sends them to MiniMax M3.1 Flash (via OpenAI-compatible API) to generate answers.

## MiniMax API

[MiniMax](https://www.minimaxi.com/) provides an OpenAI-compatible API endpoint, making it easy to integrate with existing OpenAI SDK workflows.

- **Base URL**: `https://api.minimax.io/v1`
- **Models**: `MiniMax-M3.1-Flash` (default), `MiniMax-M3`

The example uses the API's default adaptive thinking without overriding reasoning effort.
Explicit model IDs in customized requests are left unchanged.

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

## Offline request tests

Run `python -m unittest test_request` from this directory to verify the script and
notebook requests using the real SDK with a mocked HTTP transport. These tests
need `openai`, `httpx`, `beautifulsoup4`, and `requests`, but do not need an API key
or download embedding models.
