# LanceDB with NVIDIA RAG Blueprint

This example shows a **retrieval-only** integration between **LanceDB OSS** and the **NVIDIA RAG Blueprint**.
It is designed to answer a simple question for partners and alliance teams:

> Can NVIDIA's RAG software use LanceDB instead of Milvus for a real retrieval flow?

The answer is yes. NVIDIA already documents a generic custom vector database hook. This example turns that hook
into a LanceDB-specific, Docker-first reference integration that developers can follow.

## What this example includes

- `prepare_lancedb.py`: builds a small local LanceDB dataset from scratch
- automatic embeddings generated through the **LanceDB embedding registry**
- a full-text index so **hybrid search** works immediately
- `lancedb_vdb.py`: a retrieval-only LanceDB adapter for the NVIDIA blueprint `VDBRag` interface
- `docker-compose.override.yml`: example environment and volume overrides for NVIDIA's Docker deployment
- `nvidia_blueprint_changes.md`: the step-by-step NVIDIA blueprint changes needed to register LanceDB as a custom backend

## Why this is retrieval-only

NVIDIA documents two useful paths for custom vector databases:

1. full ingestion + retrieval
2. retrieval-only

The second path is the fastest credible proof. It lets you prepare documents in LanceDB first, then wire NVIDIA's
RAG server to retrieve from that collection for `/v1/search` and `/v1/generate`.

That is enough to prove that LanceDB and the NVIDIA blueprint work together without building a full ingestion stack
inside the blueprint on day one.

## Prerequisites

- Python 3.10+
- `uv`
- a clone of `NVIDIA-AI-Blueprints/rag`
- Docker if you want to run the NVIDIA services locally

## 1. Create a local `.venv` and sync dependencies

```bash
cd examples/nvidia-rag-blueprint-lancedb
uv venv .venv
source .venv/bin/activate
uv sync
```

This example is `uv`-first. The `pyproject.toml` in this directory is the source of truth for dependencies.

## 2. Build the demo LanceDB dataset

```bash
uv run prepare_lancedb.py --embedder demo-keyword --reranker mrr
```

This writes a local dataset to `./data` and creates a collection named `nvidia_blueprint_demo`.
The script also creates a full-text index on the `text` column so hybrid retrieval is available immediately.

### Optional: use a real sentence-transformers embedder

If you want to swap the offline demo embedder for a real model, set:

```bash
export LANCEDB_EMBEDDER=sentence-transformers
export LANCEDB_SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
uv run prepare_lancedb.py
```

The demo embedder exists so the example can run without depending on remote model downloads.
The NVIDIA integration itself does not depend on the demo embedder.

## 3. Patch the NVIDIA blueprint

Open [`nvidia_blueprint_changes.md`](./nvidia_blueprint_changes.md) and follow it as the source of truth for the changes you need to make in your NVIDIA RAG Blueprint checkout. It is a step-by-step change guide, not just a raw git diff.
At a minimum you need to:

- add LanceDB dependencies to the NVIDIA environment
- copy `lancedb_vdb.py` into the NVIDIA source tree
- register `APP_VECTORSTORE_NAME=lancedb` in the VDB factory

## 4. Start the NVIDIA services with LanceDB enabled

Set the path to this example so the Docker Compose override can mount the prepared LanceDB dataset:

```bash
export LANCEDB_RECIPE_DIR=$(pwd)
```

Then run the NVIDIA services from the NVIDIA repo root.

If you only want to verify retrieval and generation against an existing LanceDB collection, start the RAG server stack:

```bash
docker compose -f deploy/compose/docker-compose-rag-server.yaml -f "$LANCEDB_RECIPE_DIR"/docker-compose.override.yml   up -d --build
```

If you also want the ingestor service running alongside the RAG server, start that stack too:

```bash
docker compose   -f deploy/compose/docker-compose-ingestor-server.yaml   -f "$LANCEDB_RECIPE_DIR"/docker-compose.override.yml   up -d --build
```

For this first LanceDB example, the ingestor is optional because the integration is retrieval-only and the collection is prepared ahead of time.

### Important environment values

The override file sets these defaults:

- `APP_VECTORSTORE_NAME=lancedb`
- `APP_VECTORSTORE_URL=/opt/lancedb-recipe/data`
- `COLLECTION_NAME=nvidia_blueprint_demo`
- `APP_VECTORSTORE_SEARCHTYPE=hybrid`
- `LANCEDB_RERANKER=mrr`

`APP_VECTORSTORE_URL` is a **filesystem path** in this integration because LanceDB OSS is embedded in the NVIDIA
containers. There is no separate LanceDB server in v1.

## 5. Verify search and generation

### Search

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

### Generate

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

## Hybrid search and rerankers

This example is set up to prove more than a basic vector lookup.

- `prepare_lancedb.py` creates an FTS index so `APP_VECTORSTORE_SEARCHTYPE=hybrid` works
- the adapter supports `RRFReranker`, `MRRReranker`, and `CrossEncoderReranker`
- the default override uses `MRRReranker`, which is stronger than a plain weighted linear combination

To switch rerankers:

```bash
export LANCEDB_RERANKER=rrf
# or
export LANCEDB_RERANKER=cross-encoder
export LANCEDB_CROSS_ENCODER_MODEL=cross-encoder/ms-marco-TinyBERT-L-6
```

## What is intentionally not implemented

This example is a **retrieval-only** proof.
The following operations intentionally raise `NotImplementedError` in `lancedb_vdb.py`:

- collection creation inside NVIDIA RAG Blueprint
- document ingestion into the blueprint
- document info management APIs

Use `prepare_lancedb.py` or your own ETL process to populate LanceDB first.

## What comes next

The next logical steps are:

- carry the same adapter into a Helm/Kubernetes deployment
- swap the local demo corpus for partner-specific documents
- replace the embedded OSS path with LanceDB Enterprise or BYOC where production requirements demand it

For the first proof, though, this example keeps the story simple: **LanceDB OSS is embedded in the NVIDIA containers,
search works, hybrid retrieval works, and there is a clear trail of breadcrumbs for storage partners to follow.**
