# Improve RAG with Re-ranking
This is an example that can improve RAG search by leveraing re-ranking. For more details, please refer to
our <a href="https://blog.lancedb.com/simplest-method-to-improve-rag-pipeline-re-ranking-cf6eaec6d544"> blog post </a>.

This example shows to create a RAG application using LanceDB Cloud.

Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/RAG_Reranking/lancedb_cloud/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>


### Set credentials
if you would like to set api key through an environment variable:
```
export LANCEDB_API_KEY="sk_..."
```
or
```
import os
import getpass

os.environ["LANCEDB_API_KEY"] = getpass.getpass("Enter Your LANCEDB API Key:")
```

replace the following lines in main.py with your project slug and api key"
```
db_url="db://your-project-slug-name"
api_key="sk_..."
region="us-east-1"
```

### Run the script
```python
python main.py
```

