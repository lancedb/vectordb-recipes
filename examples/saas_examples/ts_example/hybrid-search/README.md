# Hybrid Search Example with LanceDB

This example demonstrates how to implement hybrid search using LanceDB, combining vector search and full-text search capabilities with custom reranking.

## Features

- Leverage LanceDB's build in [embedding functions API](https://lancedb.github.io/lancedb/embeddings/) to embed data and queries 
- Full-text search using LanceDB's native FTS implementation
- Hybrid search combining both vector search and FTS


## Prerequisites

- Node.js (v16 or higher)
- npm or yarn
- LanceDB Cloud account and API credentials
- OpenAI API key

## Setup

1. Clone the repository and navigate to this directory:
```bash
cd ts_example/hybrid-search
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file with your LanceDB Cloud credentials and OpenAI API key:
```bash
LANCEDB_API_KEY=your_lancedb_api_key_here
LANCEDB_URI=db://your-db-uri
OPENAI_API_KEY=your_api_key_here
```

## Running the Example

```bash
npm start
```

The example demonstrates three types of searches:
1. Pure vector search
2. Pure full-text search
3. Hybrid search with default RRF reranking


## Data Schema


## Dataset

By default, the example uses the BeIR/scidocs dataset from HuggingFace, loading documents in batches of 100. You can modify the `BATCH_SIZE` and target size in the code to load more or fewer documents.