from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
from typing import Any

import lancedb
from lancedb.embeddings import TextEmbeddingFunction, get_registry, register
from lancedb.pydantic import LanceModel, Vector
from lancedb.rerankers import CrossEncoderReranker, MRRReranker, RRFReranker

DEFAULT_DB_URI = Path(__file__).resolve().parent / "data"
DEFAULT_TABLE_NAME = "nvidia_blueprint_demo"
DEFAULT_QUERY = "How do I replace Milvus in the NVIDIA RAG blueprint with LanceDB?"
DEMO_KEYWORDS = (
    "nvidia",
    "rag",
    "lancedb",
    "milvus",
    "qdrant",
    "vector",
    "hybrid",
    "reranker",
    "storage",
    "partner",
    "kubernetes",
    "docker",
    "retrieval",
    "embedding",
    "multimodal",
)
SAMPLE_DOCUMENTS = [
    {
        "title": "NVIDIA RAG blueprint can swap vector stores",
        "source": "nvidia-change-vectordb.md",
        "document_id": "nvidia-change-vectordb-1",
        "section": "custom-vdb-overview",
        "modality": "text",
        "partner": "nvidia",
        "deployment": "docker",
        "topic": "integration",
        "text": (
            "NVIDIA RAG Blueprint includes a custom vector database integration path. "
            "Developers can replace Milvus by adding a new VDB implementation, wiring it into the factory, "
            "and setting APP_VECTORSTORE_NAME to a custom backend such as LanceDB."
        ),
    },
    {
        "title": "Retrieval-only integration is the fastest proof",
        "source": "nvidia-change-vectordb.md",
        "document_id": "nvidia-change-vectordb-2",
        "section": "retrieval-only",
        "modality": "text",
        "partner": "nvidia",
        "deployment": "docker",
        "topic": "retrieval",
        "text": (
            "NVIDIA documents a retrieval-only integration mode for custom vector stores. "
            "This path is ideal when documents are already indexed somewhere else and the goal is to prove search and generation, "
            "not to reimplement ingestion on day one."
        ),
    },
    {
        "title": "LanceDB is embedded and open source",
        "source": "lancedb-positioning.md",
        "document_id": "lancedb-positioning-1",
        "section": "embedded-oss",
        "modality": "text",
        "partner": "lancedb",
        "deployment": "embedded",
        "topic": "positioning",
        "text": (
            "LanceDB OSS runs as an embedded retrieval library instead of a standalone database server. "
            "That means a Docker or Kubernetes deployment can bake LanceDB directly into the application container, "
            "which is a good fit for NVIDIA blueprint experiments where teams want fewer moving parts."
        ),
    },
    {
        "title": "Hybrid retrieval matters for technical jargon",
        "source": "lancedb-hybrid-search.md",
        "document_id": "lancedb-hybrid-search-1",
        "section": "hybrid-search",
        "modality": "text",
        "partner": "lancedb",
        "deployment": "embedded",
        "topic": "hybrid-search",
        "text": (
            "LanceDB supports hybrid retrieval by combining dense vector search with full-text search. "
            "This is useful for NVIDIA and enterprise RAG workloads because technical jargon, product names, and partner names "
            "often need exact keyword matching alongside semantic retrieval."
        ),
    },
    {
        "title": "LanceDB supports pluggable rerankers",
        "source": "lancedb-reranking.md",
        "document_id": "lancedb-reranking-1",
        "section": "reranking",
        "modality": "text",
        "partner": "lancedb",
        "deployment": "embedded",
        "topic": "reranking",
        "text": (
            "Hybrid search in LanceDB does not stop at a weighted linear combination. "
            "It supports RRFReranker, MRRReranker, CrossEncoderReranker, and custom rerankers, "
            "which makes it a better fit for partners who want to experiment with relevance quality."
        ),
    },
    {
        "title": "Storage partners need a Milvus replacement",
        "source": "partner-migration-notes.md",
        "document_id": "partner-migration-1",
        "section": "storage-partners",
        "modality": "text",
        "partner": "weka",
        "deployment": "kubernetes",
        "topic": "partners",
        "text": (
            "WEKA, Dell, NetApp, HPE, Pure Storage, Nutanix, Hammerspace, Hitachi Vantara, and Cloudian all need a Milvus replacement path. "
            "If LanceDB provides clear Docker and Kubernetes breadcrumbs for NVIDIA blueprints, alliance teams have a concrete artifact to share."
        ),
    },
    {
        "title": "Kubernetes comes after the first Docker proof",
        "source": "delivery-plan.md",
        "document_id": "delivery-plan-1",
        "section": "milestones",
        "modality": "text",
        "partner": "lancedb",
        "deployment": "kubernetes",
        "topic": "roadmap",
        "text": (
            "The fastest path is a Docker-first proof where LanceDB is embedded in the NVIDIA containers. "
            "After that works, the same adapter can be carried into Helm and Kubernetes with a PVC or object-store-backed dataset."
        ),
    },
    {
        "title": "Enterprise is the partner-grade follow-on",
        "source": "lancedb-enterprise.md",
        "document_id": "lancedb-enterprise-1",
        "section": "byoc",
        "modality": "text",
        "partner": "lancedb",
        "deployment": "byoc",
        "topic": "enterprise",
        "text": (
            "LanceDB Enterprise extends the same open data format into a private cloud or BYOC deployment. "
            "That gives NVIDIA storage partners a path from an embedded proof of concept to production-grade serving, caching, and private networking."
        ),
    },
]


@register("demo-keyword")
class DemoKeywordEmbeddings(TextEmbeddingFunction):
    keywords: tuple[str, ...] = DEMO_KEYWORDS

    def ndims(self) -> int:
        return len(self.keywords)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        vectors: list[list[float]] = []
        for text in texts:
            lowered = text.lower()
            counts = [float(lowered.count(keyword)) for keyword in self.keywords]
            if not any(counts):
                counts[0] = 1.0
            norm = math.sqrt(sum(value * value for value in counts)) or 1.0
            vectors.append([value / norm for value in counts])
        return vectors


def build_embedder(name: str):
    registry = get_registry()
    if name == "demo-keyword":
        return registry.get("demo-keyword").create()
    if name == "sentence-transformers":
        model_name = os.environ.get(
            "LANCEDB_SENTENCE_TRANSFORMER_MODEL", "all-MiniLM-L6-v2"
        )
        return registry.get("sentence-transformers").create(name=model_name)
    raise ValueError(f"Unsupported embedder: {name}")


def build_schema(embedder):
    class BlueprintChunk(LanceModel):
        text: str = embedder.SourceField()
        vector: Vector(embedder.ndims()) = embedder.VectorField()
        title: str
        source: str
        document_id: str
        section: str
        modality: str
        partner: str
        deployment: str
        topic: str

    return BlueprintChunk


def build_reranker(name: str):
    if name == "none":
        return None
    if name == "rrf":
        return RRFReranker()
    if name == "mrr":
        return MRRReranker(weight_vector=0.65, weight_fts=0.35)
    if name == "cross-encoder":
        model_name = os.environ.get(
            "LANCEDB_CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-TinyBERT-L-6"
        )
        return CrossEncoderReranker(model_name=model_name)
    raise ValueError(f"Unsupported reranker: {name}")


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summary = []
    for row in rows:
        summary.append(
            {
                "title": row.get("title"),
                "source": row.get("source"),
                "topic": row.get("topic"),
                "deployment": row.get("deployment"),
                "score": row.get("_score"),
                "distance": row.get("_distance"),
            }
        )
    return summary


def prepare_database(uri: Path, table_name: str, embedder_name: str):
    uri.mkdir(parents=True, exist_ok=True)
    embedder = build_embedder(embedder_name)
    schema = build_schema(embedder)

    db = lancedb.connect(str(uri))
    table = db.create_table(table_name, schema=schema, mode="overwrite")
    table.add(SAMPLE_DOCUMENTS)
    table.create_fts_index("text", replace=True)

    return table


def run_preview(table, query: str, reranker_name: str, top_k: int):
    dense_results = table.search(query).limit(top_k).to_list()

    hybrid_query = table.search(query, query_type="hybrid").limit(max(top_k * 4, 8))
    reranker = build_reranker(reranker_name)
    if reranker is not None:
        hybrid_query = hybrid_query.rerank(reranker=reranker)
    hybrid_results = hybrid_query.to_list()[:top_k]

    print("\nDense search preview:")
    print(json.dumps(summarize_rows(dense_results), indent=2))

    print("\nHybrid search preview:")
    print(json.dumps(summarize_rows(hybrid_results), indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a local LanceDB dataset for the NVIDIA RAG Blueprint demo."
    )
    parser.add_argument("--uri", default=str(DEFAULT_DB_URI))
    parser.add_argument("--table-name", default=DEFAULT_TABLE_NAME)
    parser.add_argument(
        "--embedder",
        choices=["demo-keyword", "sentence-transformers"],
        default=os.environ.get("LANCEDB_EMBEDDER", "demo-keyword"),
    )
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument(
        "--reranker",
        choices=["none", "rrf", "mrr", "cross-encoder"],
        default=os.environ.get("LANCEDB_RERANKER", "mrr"),
    )
    parser.add_argument("--top-k", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    uri = Path(args.uri).expanduser().resolve()
    table = prepare_database(uri=uri, table_name=args.table_name, embedder_name=args.embedder)

    print(f"Created LanceDB dataset at: {uri}")
    print(f"Collection name: {args.table_name}")
    print(f"Rows inserted: {len(SAMPLE_DOCUMENTS)}")
    print("FTS index: text")
    run_preview(table, query=args.query, reranker_name=args.reranker, top_k=args.top_k)


if __name__ == "__main__":
    main()
