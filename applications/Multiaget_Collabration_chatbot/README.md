# Multi-Agent Collaboration Chatbot

![Multilingual-Collaboration-Chatbot](https://github.com/akashAD98/vectordb-recipes/blob/main/assets/multiagent_chatbot.png)


This project is a multi-agent collaboration chatbot designed to answer questions related to stock markets using multiple tools and APIs. It intelligently combines:

- **LanceDB**: For retrieving information from uploaded PDF documents.
- **Polygon API**: For real-time finance-related data.
- **Tavily Search**: For advanced internet search capabilities.

The chatbot is powered by **Streamlit**, providing an intuitive web interface for uploading documents and asking questions.

---

## Features

1. **PDF Document Knowledge Base**:
   - Upload stock market-related PDF files to build a knowledge base.
   - Extracts and indexes document content using **LanceDB** for quick retrieval.

2. **Tool Integration**:
   - **LanceDB**: Used for answering questions based on uploaded PDFs.
   - **Polygon API**: Fetches real-time finance-related data (e.g., stock prices, company financials).
   - **Bing Search**: Retrieves news and additional web content.
   - **Tavily Search**: Provides an advanced internet search experience.

3. **Fallback Mechanism**:
   - The chatbot first attempts to answer questions using the uploaded documents.
   - If no relevant answer is found, it intelligently switches to other tools (e.g., Polygon API, Bing, or Tavily).

4. **Streamlit Interface**:
   - User-friendly interface to upload documents, ask questions, and get responses.
---

## How It Works

### 1. Uploading Documents
Users must upload PDF files related to the stock market to build a document-based knowledge base. These documents are processed and split into manageable chunks for efficient retrieval.

### 2. Question Answering Flow
- **Document-Based Retrieval**:
  - The chatbot first searches the uploaded PDFs for an answer using **LanceDB**.
- **Fallback to Other Tools**:
  - If no relevant information is found in the documents, the chatbot uses:
    - **Polygon API**: For finance-related real-time data (e.g., stock prices, financial statements).
    - **Bing or Tavily**: For internet-based queries or news.

### Example Use Case
#### Scenario: Stock Market Q&A System
1. Upload a PDF file containing information about the stock market.
2. Ask questions like:
   - "What is gap up & down in share ?
      Answer is featched using RAG- Lancedb Tool
   - "What are the financial statements of AAPL ?"
      Answer is fetched using the Polygon Tool
   - "Latest news about the S&P 500?"
     - Answer is retrieved using Tavily Tool

---

## Prerequisites

### 1. Install Dependencies
Ensure you have Python installed and set up a virtual environment. Then, install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Set Up APIs
Obtain API keys for:
- **Polygon API** https://polygon.io/docs/stocks/getting-started
- **Tavily Search API** https://tavily.com/getting-started

Add these keys to your environment variables or configuration file.

---

## Running the Application
1. Clone the repository.
2. Navigate to the project directory.
3. Run the Streamlit application:
   ```bash
   streamlit run main.py
   ```
4. Open the provided URL in your browser.

---

## Usage Instructions

1. **Upload Documents**:
   - Drag and drop or browse to upload your stock market-related PDF files.
   - The chatbot will process and index the content.

2. **Ask Questions**:
   - Enter your question in the input box (e.g., "What are the financial statements of AAPL?").
   - The chatbot will first attempt to retrieve answers from the documents.

3. **Fallback Tools**:
   - If the answer is not found in the documents, the chatbot will use the appropriate tool:
     - **Polygon API** for finance-related data.
     - **Tavily** for internet-based search or news.
---
