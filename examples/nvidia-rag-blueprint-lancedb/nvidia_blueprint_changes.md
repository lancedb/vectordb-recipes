# NVIDIA Blueprint Changes for LanceDB

This document is the source of truth for the exact changes you need to make in your local NVIDIA RAG Blueprint checkout to use the LanceDB example. It is written as a step-by-step change guide so you can follow it even if you are new to the NVIDIA codebase.
The fastest proof is retrieval-only: prepare your LanceDB data outside the blueprint, then wire
LanceDB into the RAG server so `/v1/search` and `/v1/generate` retrieve from it.

## 1. Add dependencies

Add these packages to the NVIDIA blueprint `pyproject.toml`:

```toml
lancedb = ">=0.30.0"
langchain-core = ">=0.3.0"
pyarrow = ">=14.0.0"
pandas = ">=2.0.0"
```

If you want to use `LANCEDB_RERANKER=cross-encoder`, also ensure the environment already includes
`sentence-transformers`.

## 2. Copy the adapter into the NVIDIA repo

Copy this example adapter into the blueprint source tree:

```bash
mkdir -p src/nvidia_rag/utils/vdb/lancedb
cp /path/to/vectordb-recipes/examples/nvidia-rag-blueprint-lancedb/lancedb_vdb.py \
  src/nvidia_rag/utils/vdb/lancedb/lancedb.py
```

## 3. Register the backend in the VDB factory

Update `src/nvidia_rag/utils/vdb/__init__.py`:

```diff
+from .lancedb.lancedb import LanceDBVDB
+
 def _get_vdb_op(vdb_endpoint, collection_name, embedding_model=None):
     ...
+    if CONFIG.vector_store.name == "lancedb":
+        return LanceDBVDB(
+            vdb_endpoint or CONFIG.vector_store.url,
+            collection_name,
+            embedding_model,
+        )
```

The exact file structure in NVIDIA's repo may evolve. The important part is that the `lancedb`
branch is resolved in the same factory that currently instantiates the Milvus and Elasticsearch
operators.

## 4. Prepare the LanceDB data separately

From this example directory:

```bash
uv venv .venv
source .venv/bin/activate
uv sync
uv run prepare_lancedb.py --embedder demo-keyword
```

That creates a local dataset under `data/` with:

- collection name: `nvidia_blueprint_demo`
- automatic embeddings generated via the LanceDB embedding registry
- a full-text index on `text`

## 5. Run the NVIDIA services with LanceDB enabled

Set the recipe directory so the override file can mount the prepared data into the NVIDIA containers:

```bash
export LANCEDB_RECIPE_DIR=/absolute/path/to/vectordb-recipes/examples/nvidia-rag-blueprint-lancedb
```

Then run the blueprint's Docker Compose deployment with this example's override file:

```bash
docker compose \
  -f deploy/compose/docker-compose-rag-server.yaml \
  -f "$LANCEDB_RECIPE_DIR"/docker-compose.override.yml \
  up -d --build

docker compose \
  -f deploy/compose/docker-compose-ingestor-server.yaml \
  -f "$LANCEDB_RECIPE_DIR"/docker-compose.override.yml \
  up -d --build
```

The important environment values are:

- `APP_VECTORSTORE_NAME=lancedb`
- `APP_VECTORSTORE_URL=/opt/lancedb-recipe/data`
- `COLLECTION_NAME=nvidia_blueprint_demo`
- `APP_VECTORSTORE_SEARCHTYPE=hybrid`
- `LANCEDB_RERANKER=mrr`

`APP_VECTORSTORE_URL` is a filesystem path in this integration, not an HTTP endpoint.

## 6. Verify retrieval and generation

Once the servers are up, verify the search path:

```bash
curl -X POST http://localhost:8081/v1/search \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "How do I replace Milvus in the NVIDIA RAG blueprint with LanceDB?",
    "use_knowledge_base": true,
    "collection_names": ["nvidia_blueprint_demo"],
    "vdb_top_k": 3,
    "reranker_top_k": 0
  }'
```

Then verify generation:

```bash
curl -N -X POST http://localhost:8081/v1/generate \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [{"role":"user","content":"Summarize the LanceDB integration approach."}],
    "use_knowledge_base": true,
    "collection_names": ["nvidia_blueprint_demo"],
    "vdb_top_k": 3,
    "reranker_top_k": 0
  }'
```

## 7. Retrieval-only boundaries

This adapter intentionally does **not** implement ingestion into NVIDIA RAG Blueprint.
The following methods raise `NotImplementedError` on purpose:

- `create_collection()`
- `write_to_index()`
- document-info management methods

For the first proof, the ingestion path is handled by `prepare_lancedb.py` or your own external data prep job.
