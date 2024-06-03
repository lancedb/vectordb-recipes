# Benchmarking Cohere Rerankers with LanceDB

<img width="1000" alt="Screenshot-2024-05-06-at-6 06 30-PM" src="https://github.com/lancedb/vectordb-recipes/assets/15766192/fe831af0-9ba4-484e-8ba2-099b5484c435">

### [Read the blog](https://blog.lancedb.com/benchmarking-cohere-reranker-with-lancedb/)

## Setup
```
pip install -r requirements.txt
```

Download the desired dataset. For example, Uber10K
!llamaindex-cli download-llamadataset Uber10KDataset2021 --download-dir ./data

## Run the benchmark
`COHERE_API_KEY=... OPENAI_API_KEY=... python main.py`

