from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any

model_cache = {}


def get_embedding_model(model_name: str) -> SentenceTransformer:
    if model_name not in model_cache:
        print(f"Loading embedding model: {model_name}...")
        model_cache[model_name] = SentenceTransformer(model_name)
    return model_cache[model_name]


def embed_documents(
    model: SentenceTransformer, docs: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    if not docs:
        return []

    print(f"Embedding {len(docs)} documents...")

    texts_to_embed = [doc.get("abstract") or doc.get("title", "") for doc in docs]

    valid_docs = [doc for doc, text in zip(docs, texts_to_embed) if text]
    valid_texts = [text for text in texts_to_embed if text]

    if not valid_texts:
        print("No valid text found in documents to embed.")
        return []

    embeddings = model.encode(valid_texts, show_progress_bar=True)

    data_for_db = []
    for i, doc in enumerate(valid_docs):
        data_for_db.append(
            {
                "vector": embeddings[i],
                "title": doc.get("title", "N/A"),
                "abstract": doc.get("abstract", "N/A"),
                "publication_date": doc.get("publication_date"),
                "url": doc.get("html_url"),
                "doc_id": doc.get("document_number"),
            }
        )

    print(f"Successfully embedded {len(data_for_db)} documents.")
    return data_for_db
