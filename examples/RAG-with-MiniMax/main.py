"""
RAG with MiniMax and LanceDB

Demonstrates a Retrieval-Augmented Generation pipeline using:
- sentence-transformers for embeddings
- LanceDB for vector storage and retrieval
- MiniMax M2.7 (via OpenAI-compatible API) for answer generation
"""

import json
import os
import re

import lancedb
import pandas as pd
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from sentence_transformers import SentenceTransformer


def scrape_content(url: str) -> str:
    """Scrape text content from a web page."""
    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join(para.get_text() for para in paragraphs)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""


def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    """Split text into fixed-size chunks by sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    chunks, current = [], ""
    for sentence in sentences:
        if len(current) + len(sentence) > chunk_size and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current = f"{current} {sentence}" if current else sentence
    if current.strip():
        chunks.append(current.strip())
    return chunks


def build_vector_store(urls: list[str], db_path: str = "lancedb_minimax"):
    """Scrape URLs, generate embeddings, and store in LanceDB."""
    model = SentenceTransformer("all-MiniLM-L6-v2")

    all_chunks = []
    all_embeddings = []

    for url in urls:
        print(f"Scraping: {url}")
        content = scrape_content(url)
        if not content or len(content) < 50:
            print(f"  Skipped (too short)")
            continue
        chunks = chunk_text(content)
        for chunk in chunks:
            if len(chunk.strip()) < 20:
                continue
            embedding = model.encode(chunk)
            all_chunks.append(chunk)
            all_embeddings.append(embedding)

    print(f"\nTotal chunks indexed: {len(all_chunks)}")

    df = pd.DataFrame({"vector": all_embeddings, "text": all_chunks})
    db = lancedb.connect(db_path)
    table = db.create_table("rag_docs", data=df, mode="overwrite")
    return table


def retrieve(query: str, table, top_k: int = 5) -> list[str]:
    """Retrieve the top-k most relevant chunks for a query."""
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode(query)
    results = table.search(query_embedding).limit(top_k).to_pandas()
    return list(results["text"])


def ask_minimax(query: str, context_docs: list[str]) -> str:
    """Send a RAG query to MiniMax M2.7 via OpenAI-compatible API."""
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable is not set")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.minimax.io/v1",
    )

    context = "\n\n---\n\n".join(context_docs)
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Answer the user's question based on "
                "the provided context. If the context does not contain enough "
                "information, say so clearly."
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {query}",
        },
    ]

    response = client.chat.completions.create(
        model="MiniMax-M2.7",
        messages=messages,
        temperature=0.7,
        max_tokens=1024,
    )
    return response.choices[0].message.content


def main():
    # Example: scrape LanceDB documentation pages
    urls = [
        "https://lancedb.github.io/lancedb/",
        "https://lancedb.github.io/lancedb/basic/",
        "https://lancedb.github.io/lancedb/concepts/vector_search/",
    ]

    print("=== Building vector store ===")
    table = build_vector_store(urls)

    print("\n=== Querying with MiniMax RAG ===")
    query = "What is LanceDB and how does vector search work?"
    print(f"Query: {query}\n")

    docs = retrieve(query, table)
    print(f"Retrieved {len(docs)} relevant chunks\n")

    answer = ask_minimax(query, docs)
    print(f"MiniMax Answer:\n{answer}")


if __name__ == "__main__":
    main()
