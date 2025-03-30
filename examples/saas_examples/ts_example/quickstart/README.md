# LanceDB Cloud Quickstart - TypeScript

🚀 **_If you haven’t signed up for LanceDB Cloud yet, click [here](https://cloud.lancedb.com) to get started!_**

This project demonstrates how to use LanceDB Cloud with TypeScript to create a semantic search application using the AG News dataset and Hugging Face's transformers.

## Features

- 📚 Integration with AG News dataset from Hugging Face
- 🚀 Vector similarity search with LanceDB Cloud
- ⚡ Efficient vector indexing with IVF-PQ

## Prerequisites

- Node.js (v16 or later)
- npm or yarn
- LanceDB Cloud account and API credentials

## Setup

1. Clone the repository and navigate to the project directory:
```bash
cd ts_example/quickstart
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file in the project root with your LanceDB Cloud credentials:
```env
LANCEDB_URI=db://your_lancedb_uri
LANCEDB_API_KEY=your_api_key
```

## Usage

### Basic Example
Run the AG News dataset example:
```bash
npm start
```

This will:
1. Load articles from the AG News dataset
2. Create a LanceDB table
3. Perform a semantic search with an example query


### Vector Dimensions
- Embedding size: 768
- Distance metric: Cosine similarity

### Dependencies

- `@lancedb/lancedb`: Vector database client
- `apache-arrow`: Data structure handling
- `dotenv`: Environment configuration

## Notes

- The AG News example uses a default limit of 1000 articles
- The index creation process is asynchronous and may take a couple of minutes