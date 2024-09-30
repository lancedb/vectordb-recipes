# Lancedb Embeddings API: Multi-lingual semantic search
In this example, we'll build a simple LanceDB table containing embeddings for different languages that can be used for universal semantic search.
* The **Dataset** used will be wikipedia dataset in English and French
* The **Model** used will be cohere's multi-lingual model

In this example, we'll explore LanceDB's Embeddings API that allows you to create tables that automatically vectorize data once you define the config at the time of table creation. Let's dive right in!

To learn more about LanceDB, visit [our docs](https://lancedb.github.io/lancedb/)

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multi-lingual-wiki-qa/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

Run python script:
```
COHERE_API_KEY=... python main.py
```