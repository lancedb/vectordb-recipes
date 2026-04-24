"""
Integration tests for RAG with MiniMax example.

These tests require a valid MINIMAX_API_KEY environment variable.
Skip automatically if the key is not set.
"""

import os
import re
import tempfile
import unittest

import lancedb
import numpy as np
import pandas as pd

MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
SKIP_REASON = "MINIMAX_API_KEY not set"


def chunk_text(text: str, chunk_size: int = 500) -> list:
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


class TestMiniMaxIntegration(unittest.TestCase):
    """Integration tests that call the real MiniMax API."""

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_basic_chat_completion(self):
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )
        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[{"role": "user", "content": "Say hello in one word."}],
            temperature=0.7,
            max_tokens=10,
        )
        self.assertIsNotNone(response.choices)
        self.assertGreater(len(response.choices), 0)
        self.assertIsNotNone(response.choices[0].message.content)

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_rag_query_with_context(self):
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )

        context = (
            "LanceDB is an open-source vector database designed for AI applications. "
            "It supports fast similarity search using vector embeddings. "
            "LanceDB integrates natively with Python data tools like pandas and PyArrow."
        )
        query = "What is LanceDB?"

        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[
                {
                    "role": "system",
                    "content": "Answer based on the provided context only.",
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
            temperature=0.7,
            max_tokens=256,
        )

        answer = response.choices[0].message.content
        self.assertIsNotNone(answer)
        self.assertGreater(len(answer), 10)

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_highspeed_model(self):
        from openai import OpenAI

        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )
        response = client.chat.completions.create(
            model="MiniMax-M2.7-highspeed",
            messages=[{"role": "user", "content": "What is 2+2?"}],
            temperature=0.5,
            max_tokens=10,
        )
        answer = response.choices[0].message.content
        self.assertIsNotNone(answer)


class TestEndToEndPipeline(unittest.TestCase):
    """End-to-end pipeline test with LanceDB + MiniMax."""

    @unittest.skipUnless(MINIMAX_API_KEY, SKIP_REASON)
    def test_full_rag_pipeline(self):
        from openai import OpenAI

        # Prepare documents
        docs = [
            "Python is a popular programming language used in AI and data science.",
            "LanceDB provides serverless vector search with no infrastructure to manage.",
            "MiniMax M2.7 is a large language model with 1M token context window.",
        ]

        # Create embeddings (use random vectors for speed; real pipeline uses sentence-transformers)
        dim = 384
        vectors = [np.random.randn(dim).astype(np.float32) for _ in docs]

        # Store in LanceDB
        tmpdir = tempfile.mkdtemp()
        db = lancedb.connect(tmpdir)
        df = pd.DataFrame({"vector": vectors, "text": docs})
        table = db.create_table("e2e_test", data=df, mode="overwrite")

        # Retrieve
        query_vec = np.random.randn(dim).astype(np.float32)
        results = table.search(query_vec).limit(2).to_pandas()
        context = "\n\n".join(list(results["text"]))

        # Query MiniMax
        client = OpenAI(
            api_key=MINIMAX_API_KEY,
            base_url="https://api.minimax.io/v1",
        )
        response = client.chat.completions.create(
            model="MiniMax-M2.7",
            messages=[
                {"role": "system", "content": "Answer based on context."},
                {"role": "user", "content": f"Context:\n{context}\n\nSummarize the context."},
            ],
            temperature=0.7,
            max_tokens=128,
        )

        answer = response.choices[0].message.content
        self.assertIsNotNone(answer)
        self.assertGreater(len(answer), 5)


if __name__ == "__main__":
    unittest.main()
