## Locally RAG from Scratch with Llama3

This  example demonstrates RAG built from scratch without using any supporting framework like Langchain and LlamaIndex. 

![alt text](<../../assets/RAG-locally.png>)

This easy to build RAG locally can be done in following steps:

1. Reading Document and Recursive Text Splitting
2. Setup LanceDB table with schema and LanceDB Embedding API
3. Insert Chunks in LanceDB table
4. Query your question(This step will do semantic search and use Llama3 llm for resulting output)

**NOTE:** You can change document and query in document both in `rag.py`, Try to run with your custom document with your custom query questions.