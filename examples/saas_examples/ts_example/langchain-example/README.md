# Reducing Hallucinations from AI Agents using Long-Term Memory

## Introduction

AI agents can help simplify and automate tedious workflows, but they often hallucinate or provide incorrect information. This example demonstrates how to reduce hallucinations from AI agents by using critique-based contexting with LanceDB Cloud as a long-term memory database.

The application works as a fitness trainer that:
1. Receives user information and fitness interests
2. Searches for relevant information using a search tool
3. Retrieves previous similar queries and their critiques from LanceDB Cloud
4. Provides personalized fitness advice
5. Stores the actions taken and critiques for future improvement

## Prerequisites

- Node.js 16+
- npm or yarn
- OpenAI API key (for LLM and embeddings)
- LanceDB Cloud API key and URI
- SerpAPI key (optional, for search functionality)

Note that SerpAPI is used to validate/correct the AI agent's answers by searching for the latest information.

## Setup

1. Clone the repository and install dependencies:
```bash
cd ts_example/langchain-new
npm install
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY=your_openai_api_key
export LANCEDB_API_KEY=your_lancedb_cloud_api_key
export LANCEDB_URI=db://region.lancedb.cloud/organization/database
export SERPAPI_API_KEY=your_serpapi_api_key  # Optional
```

## Running the Example

```bash
npm start
```

When prompted, enter your fitness information and interests. For example:
```
Tell us about you and your fitness interests: university student, loves running
```

The agent will:
1. Retrieve any past similar queries and review critiques
2. Search for relevant fitness information
3. Generate a personalized fitness routine
4. Store the actions and critiques in LanceDB Cloud for future improvement


## How It Works

The system uses:
- **LangChain** for agent orchestration and vector store abstraction
- **LanceDB Cloud** for efficient cloud-based vector storage and retrieval
- **OpenAI** for embeddings and LLM functionality

The critique-based contexting pattern helps improve responses by:
1. Storing a history of past agent actions and critiques as document embeddings
2. Retrieving relevant past examples using semantic similarity search
3. Incorporating these critiques into new responses
4. Continuously improving as more interactions are stored

