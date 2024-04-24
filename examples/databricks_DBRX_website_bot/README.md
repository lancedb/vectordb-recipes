## Hogwarts chatbot with Open source RAG using DBRX, LanceDB, and LLama-index with Hugginface Embeddings

This application is a website chatbot that uses the Open source RAG model with DBRX, LanceDB, and LLama-index with Hugginface Embeddings. The chatbot is built using the RAG model, which is a retrieval-augmented generation model that can be used for a variety of tasks, including question answering, text generation, and more.

### Steps to Run the Application

1. Install Dependencies
```
pip install -r requirements.txt
```

2. Setup Databricks Serving Endpoint and token as environment variables for using databricks serving endpoint. You can also use the dbrx model locally as it is open source.
```
export DATABRICKS_API_KEY=<your api key>
DATABRICKS_SERVING_ENDPOINT=<your api serving endpoint>
```

3. Run the application
```
python main.py
```

Accepted arguments:
- `url`: URL of the document to be indexed. Default is the Hogwarts School of Witchcraft and Wizardry Wikipedia page.
- `embed_model`: Huggingface model to use for embeddings. Default is `mixedbread-ai/mxbai-embed-large-v1`.
- `uri`: URI of the vector store. Default is `~/tmp/lancedb_hogwarts`.
- `force_create_embeddings`: Whether to force create embeddings. Default is `False`.
