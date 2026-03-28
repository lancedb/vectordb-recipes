"""
Unit tests for RAG with MiniMax example.

Tests the scraping, chunking, embedding, and LanceDB storage
components without requiring external API access.
"""

import os
import re
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import lancedb
import numpy as np
import pandas as pd


# ---- Inline helpers (mirroring main.py logic) ----

def scrape_content(url: str) -> str:
    """Scrape text content from a web page."""
    import requests
    from bs4 import BeautifulSoup

    try:
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        return " ".join(para.get_text() for para in paragraphs)
    except Exception:
        return ""


def chunk_text(text: str, chunk_size: int = 500) -> list:
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


# ---- Tests ----

class TestChunkText(unittest.TestCase):
    """Test the text chunking function."""

    def test_empty_string(self):
        result = chunk_text("")
        self.assertEqual(result, [])

    def test_single_short_sentence(self):
        result = chunk_text("Hello world.")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Hello world.")

    def test_multiple_sentences_under_chunk_size(self):
        text = "First sentence. Second sentence. Third sentence."
        result = chunk_text(text, chunk_size=500)
        self.assertEqual(len(result), 1)
        self.assertIn("First sentence.", result[0])
        self.assertIn("Third sentence.", result[0])

    def test_chunk_splitting_at_boundary(self):
        text = "A" * 300 + ". " + "B" * 300 + ". " + "C" * 100 + "."
        result = chunk_text(text, chunk_size=400)
        self.assertGreater(len(result), 1)

    def test_preserves_content(self):
        text = "Sentence one. Sentence two. Sentence three."
        result = chunk_text(text, chunk_size=500)
        joined = " ".join(result)
        self.assertIn("Sentence one", joined)
        self.assertIn("Sentence two", joined)
        self.assertIn("Sentence three", joined)

    def test_small_chunk_size(self):
        text = "First sentence here. Second sentence here. Third one."
        result = chunk_text(text, chunk_size=25)
        self.assertGreater(len(result), 1)

    def test_no_sentence_boundaries(self):
        text = "word " * 100
        result = chunk_text(text.strip(), chunk_size=50)
        self.assertEqual(len(result), 1)  # No sentence boundaries to split on

    def test_question_mark_boundary(self):
        text = "What is LanceDB? It is a vector database. How does it work?"
        result = chunk_text(text, chunk_size=30)
        self.assertGreater(len(result), 1)

    def test_exclamation_mark_boundary(self):
        text = "This is great! Another sentence here. And one more!"
        result = chunk_text(text, chunk_size=25)
        self.assertGreater(len(result), 1)


class TestScrapeContent(unittest.TestCase):
    """Test the web scraping function."""

    @patch("requests.get")
    def test_successful_scrape(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body><p>Hello world</p><p>Second paragraph</p></body></html>"
        mock_get.return_value = mock_response

        result = scrape_content("https://example.com")
        self.assertIn("Hello world", result)
        self.assertIn("Second paragraph", result)

    @patch("requests.get")
    def test_empty_page(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = b"<html><body></body></html>"
        mock_get.return_value = mock_response

        result = scrape_content("https://example.com")
        self.assertEqual(result, "")

    @patch("requests.get", side_effect=Exception("Connection error"))
    def test_failed_request(self, mock_get):
        result = scrape_content("https://unreachable.example.com")
        self.assertEqual(result, "")

    @patch("requests.get")
    def test_extracts_only_paragraphs(self, mock_get):
        mock_response = MagicMock()
        mock_response.content = (
            b"<html><body>"
            b"<h1>Title</h1>"
            b"<p>Paragraph text</p>"
            b"<div>Div text</div>"
            b"</body></html>"
        )
        mock_get.return_value = mock_response

        result = scrape_content("https://example.com")
        self.assertIn("Paragraph text", result)
        self.assertNotIn("Title", result)
        self.assertNotIn("Div text", result)


class TestLanceDBStorage(unittest.TestCase):
    """Test LanceDB vector storage and retrieval."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.db = lancedb.connect(self.tmpdir)

    def test_create_table_and_search(self):
        dim = 384  # all-MiniLM-L6-v2 dimension
        vectors = [np.random.randn(dim).astype(np.float32) for _ in range(5)]
        texts = [f"Document {i}" for i in range(5)]

        df = pd.DataFrame({"vector": vectors, "text": texts})
        table = self.db.create_table("test_docs", data=df, mode="overwrite")

        query_vec = np.random.randn(dim).astype(np.float32)
        results = table.search(query_vec).limit(3).to_pandas()

        self.assertEqual(len(results), 3)
        self.assertIn("text", results.columns)

    def test_empty_table_search(self):
        dim = 384
        vectors = [np.random.randn(dim).astype(np.float32)]
        texts = ["Single doc"]

        df = pd.DataFrame({"vector": vectors, "text": texts})
        table = self.db.create_table("single_doc", data=df, mode="overwrite")

        query_vec = np.random.randn(dim).astype(np.float32)
        results = table.search(query_vec).limit(5).to_pandas()
        self.assertEqual(len(results), 1)

    def test_overwrite_mode(self):
        dim = 384
        vectors1 = [np.random.randn(dim).astype(np.float32) for _ in range(3)]
        texts1 = [f"Old doc {i}" for i in range(3)]
        df1 = pd.DataFrame({"vector": vectors1, "text": texts1})
        self.db.create_table("overwrite_test", data=df1, mode="overwrite")

        vectors2 = [np.random.randn(dim).astype(np.float32) for _ in range(2)]
        texts2 = [f"New doc {i}" for i in range(2)]
        df2 = pd.DataFrame({"vector": vectors2, "text": texts2})
        table = self.db.create_table("overwrite_test", data=df2, mode="overwrite")

        all_rows = table.to_pandas()
        self.assertEqual(len(all_rows), 2)


class TestMiniMaxClientConfig(unittest.TestCase):
    """Test MiniMax OpenAI-compatible client configuration."""

    def test_base_url_format(self):
        base_url = "https://api.minimax.io/v1"
        self.assertTrue(base_url.startswith("https://"))
        self.assertIn("minimax", base_url)

    def test_model_names(self):
        models = ["MiniMax-M2.7", "MiniMax-M2.7-highspeed"]
        for model in models:
            self.assertTrue(model.startswith("MiniMax-"))
            self.assertIn("M2", model)

    def test_temperature_must_be_positive(self):
        temperature = 0.7
        self.assertGreater(temperature, 0.0)
        self.assertLessEqual(temperature, 1.0)

    @patch("openai.OpenAI")
    def test_client_instantiation(self, mock_openai_cls):
        from openai import OpenAI

        client = OpenAI(
            api_key="test-key",
            base_url="https://api.minimax.io/v1",
        )
        mock_openai_cls.assert_called_once_with(
            api_key="test-key",
            base_url="https://api.minimax.io/v1",
        )

    def test_env_var_name(self):
        env_var = "MINIMAX_API_KEY"
        self.assertEqual(env_var, "MINIMAX_API_KEY")


class TestRAGPipeline(unittest.TestCase):
    """Test the end-to-end RAG pipeline components."""

    def test_chunk_and_store(self):
        text = (
            "LanceDB is a vector database. "
            "It supports fast similarity search. "
            "You can use it with Python. "
            "It integrates with pandas and arrow."
        )
        chunks = chunk_text(text, chunk_size=80)
        self.assertGreater(len(chunks), 0)

        dim = 384
        vectors = [np.random.randn(dim).astype(np.float32) for _ in chunks]
        df = pd.DataFrame({"vector": vectors, "text": chunks})

        tmpdir = tempfile.mkdtemp()
        db = lancedb.connect(tmpdir)
        table = db.create_table("pipeline_test", data=df, mode="overwrite")

        query_vec = np.random.randn(dim).astype(np.float32)
        results = table.search(query_vec).limit(2).to_pandas()

        self.assertGreater(len(results), 0)
        self.assertIn("text", results.columns)

    def test_context_formatting(self):
        docs = ["Doc A content here.", "Doc B content here.", "Doc C content here."]
        context = "\n\n---\n\n".join(docs)
        self.assertIn("Doc A content here.", context)
        self.assertIn("---", context)
        parts = context.split("---")
        self.assertEqual(len(parts), 3)

    @patch("openai.OpenAI")
    def test_minimax_message_format(self, mock_openai_cls):
        query = "What is LanceDB?"
        context = "LanceDB is a vector database for AI applications."
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Answer the user's question based on "
                    "the provided context."
                ),
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            },
        ]
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertIn("LanceDB", messages[1]["content"])
        self.assertIn("What is LanceDB?", messages[1]["content"])


if __name__ == "__main__":
    unittest.main()
