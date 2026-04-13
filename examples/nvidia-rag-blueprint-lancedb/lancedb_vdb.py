from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any

import lancedb
from langchain_core.documents import Document
from lancedb.embeddings import TextEmbeddingFunction, register
from lancedb.rerankers import CrossEncoderReranker, MRRReranker, RRFReranker

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


class LanceDBVDB:
    """Retrieval-only LanceDB adapter for NVIDIA RAG Blueprint.

    Copy this file into `src/nvidia_rag/utils/vdb/lancedb/lancedb.py` inside the
    NVIDIA blueprint repository and register it in the VDB factory.
    """

    def __init__(
        self,
        vdb_endpoint: str,
        collection_name: str,
        embedding_model: Any = None,
    ) -> None:
        if not vdb_endpoint:
            raise ValueError("vdb_endpoint must point to a local LanceDB directory")

        endpoint = Path(vdb_endpoint).expanduser().resolve()
        self.vdb_endpoint = str(endpoint)
        self.collection_name = collection_name or os.environ.get(
            "COLLECTION_NAME", "nvidia_blueprint_demo"
        )
        self.embedding_model = embedding_model
        self.search_type = os.environ.get("APP_VECTORSTORE_SEARCHTYPE", "dense").lower()
        self.reranker_name = os.environ.get("LANCEDB_RERANKER", "rrf").lower()
        self.candidate_multiplier = int(
            os.environ.get("LANCEDB_RETRIEVAL_CANDIDATES", "4")
        )
        self.cross_encoder_model = os.environ.get(
            "LANCEDB_CROSS_ENCODER_MODEL", "cross-encoder/ms-marco-TinyBERT-L-6"
        )
        self._db = lancedb.connect(self.vdb_endpoint)

    def close(self) -> None:
        self._db = None

    def __enter__(self) -> "LanceDBVDB":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        self.close()
        return False

    def check_health(self) -> dict[str, Any]:
        tables = self._db.table_names()
        return {
            "status": "ok",
            "endpoint": self.vdb_endpoint,
            "collections": tables,
        }

    def get_collection(self) -> list[dict[str, Any]]:
        collections = []
        for name in self._db.table_names():
            table = self._db.open_table(name)
            collections.append({"name": name, "row_count": len(table)})
        return collections

    def check_collection_exists(self, collection_name: str) -> bool:
        return collection_name in self._db.table_names()

    def get_langchain_vectorstore(self, collection_name: str):
        if not self.check_collection_exists(collection_name):
            return None
        return self._db.open_table(collection_name)

    def retrieval_langchain(
        self,
        query: str,
        collection_name: str,
        vectorstore=None,
        top_k: int = 10,
        filter_expr: str = "",
        otel_ctx=None,
    ) -> list[Document]:
        table = vectorstore or self.get_langchain_vectorstore(
            collection_name or self.collection_name
        )
        if table is None:
            raise ValueError(f"Collection does not exist: {collection_name}")

        query_builder = self._build_query(
            table=table,
            query=query,
            top_k=top_k,
            filter_expr=filter_expr,
        )
        rows = query_builder.to_list()
        if self.search_type == "hybrid":
            rows = rows[:top_k]
        return [
            self._to_document(row, collection_name or self.collection_name)
            for row in rows
        ]

    def _build_query(self, table, query: str, top_k: int, filter_expr: str):
        candidate_count = max(top_k * self.candidate_multiplier, top_k)
        if self.search_type == "hybrid":
            builder = table.search(query, query_type="hybrid")
            if filter_expr:
                builder = builder.where(filter_expr, prefilter=True)
            builder = builder.limit(candidate_count)
            reranker = self._build_reranker()
            if reranker is not None:
                builder = builder.rerank(reranker=reranker)
            return builder

        builder = table.search(query)
        if filter_expr:
            builder = builder.where(filter_expr, prefilter=True)
        return builder.limit(top_k)

    def _build_reranker(self):
        if self.reranker_name == "none":
            return None
        if self.reranker_name == "rrf":
            return RRFReranker()
        if self.reranker_name == "mrr":
            return MRRReranker(weight_vector=0.65, weight_fts=0.35)
        if self.reranker_name == "cross-encoder":
            return CrossEncoderReranker(model_name=self.cross_encoder_model)
        raise ValueError(f"Unsupported LANCEDB_RERANKER value: {self.reranker_name}")

    def _to_document(self, row: dict[str, Any], collection_name: str) -> Document:
        content_metadata = {
            key: row[key]
            for key in ("topic", "partner", "deployment", "modality", "section")
            if key in row and row[key] is not None
        }
        if row.get("_score") is not None:
            content_metadata["score"] = row["_score"]
        if row.get("_distance") is not None:
            content_metadata["distance"] = row["_distance"]

        metadata = {
            "source": row.get("source", "unknown"),
            "content_metadata": content_metadata,
            "collection_name": collection_name,
        }
        if row.get("title") is not None:
            metadata["title"] = row["title"]
        if row.get("document_id") is not None:
            metadata["document_id"] = row["document_id"]

        return Document(page_content=row.get("text", ""), metadata=metadata)

    def create_collection(self, *args, **kwargs):
        raise NotImplementedError("This example is retrieval-only. Prepare data separately.")

    def write_to_index(self, *args, **kwargs):
        raise NotImplementedError("This example is retrieval-only. Prepare data separately.")

    def create_document_info_collection(self, *args, **kwargs):
        raise NotImplementedError("This example is retrieval-only. Prepare data separately.")

    def add_document_info(self, *args, **kwargs):
        raise NotImplementedError("This example is retrieval-only. Prepare data separately.")

    def get_document_info(self, *args, **kwargs):
        raise NotImplementedError("This example is retrieval-only. Prepare data separately.")
