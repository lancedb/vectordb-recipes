"""Offline tests of the example's real SDK requests; no embedding downloads."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

import httpx
from openai import OpenAI

EXAMPLE_DIR = Path(__file__).parent


class TestMiniMaxRequests(unittest.TestCase):
    def setUp(self):
        self.requests = []

        def respond(request):
            self.requests.append(request)
            return httpx.Response(
                200,
                json={
                    "id": "offline-completion",
                    "object": "chat.completion",
                    "created": 0,
                    "model": "MiniMax-M3.1-Flash",
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": "Test answer"},
                            "finish_reason": "stop",
                        }
                    ],
                },
            )

        self.http_client = httpx.Client(transport=httpx.MockTransport(respond))
        self.addCleanup(self.http_client.close)
        # Only the unrelated vector/embedding imports are mocked. Requests use
        # the actual OpenAI SDK and its JSON serialization through MockTransport.
        with patch.dict(
            sys.modules,
            {
                "lancedb": MagicMock(),
                "pandas": MagicMock(),
                "sentence_transformers": MagicMock(),
            },
        ):
            spec = importlib.util.spec_from_file_location(
                "minimax_example", EXAMPLE_DIR / "main.py"
            )
            self.example = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.example)
        self.env = patch.dict(
            os.environ, {"MINIMAX_API_KEY": "offline-test"}, clear=True
        )
        self.env.start()
        self.addCleanup(self.env.stop)

    def make_client(self, **kwargs):
        return OpenAI(**kwargs, http_client=self.http_client, max_retries=0)

    def assert_request(self, request, question, context):
        self.assertEqual(request.method, "POST")
        self.assertEqual(str(request.url), "https://api.minimax.io/v1/chat/completions")
        payload = json.loads(request.content)
        self.assertEqual(
            set(payload), {"model", "messages", "temperature", "max_tokens"}
        )
        self.assertEqual(payload["model"], "MiniMax-M3.1-Flash")
        self.assertEqual(payload["temperature"], 0.7)
        self.assertEqual(payload["max_tokens"], 1024)
        self.assertEqual(payload["messages"][0]["role"], "system")
        self.assertEqual(
            payload["messages"][1],
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        )
        return payload

    def test_default_script_path(self):
        docs = ["First context", "Second context"]
        with (
            patch.object(self.example, "OpenAI", side_effect=self.make_client),
            patch.object(self.example, "build_vector_store"),
            patch.object(self.example, "retrieve", return_value=docs),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.example.main()
        self.assertIn("Test answer", output.getvalue())
        self.assertEqual(len(self.requests), 1)
        self.assert_request(
            self.requests[0],
            "What is LanceDB and how does vector search work?",
            "\n\n---\n\n".join(docs),
        )

    def test_missing_key_fails_before_transport(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "MINIMAX_API_KEY"):
                self.example.ask_minimax("Question", [])
        self.assertEqual(self.requests, [])

    def test_explicit_legacy_integration_request_is_preserved(self):
        with patch.dict(
            sys.modules,
            {"lancedb": MagicMock(), "pandas": MagicMock(), "numpy": MagicMock()},
        ):
            spec = importlib.util.spec_from_file_location(
                "minimax_integration", EXAMPLE_DIR / "test_integration.py"
            )
            integration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(integration)
        with patch("openai.OpenAI", side_effect=self.make_client):
            integration.TestMiniMaxIntegration(
                "test_highspeed_model"
            ).test_highspeed_model()
        self.assertEqual(len(self.requests), 1)
        payload = json.loads(self.requests[0].content)
        self.assertEqual(payload["model"], "MiniMax-M2.7-highspeed")
        self.assertEqual(
            payload["messages"], [{"role": "user", "content": "What is 2+2?"}]
        )

    def test_notebook_request_cells(self):
        notebook = json.loads((EXAMPLE_DIR / "RAG_with_MiniMax.ipynb").read_text())
        request_cells = [
            "".join(cell["source"])
            for cell in notebook["cells"]
            if cell["cell_type"] == "code"
            and "client.chat.completions.create(" in "".join(cell["source"])
        ]
        self.assertEqual(len(request_cells), 2)
        table = MagicMock()
        table.search.return_value.limit.return_value.to_pandas.return_value = {
            "text": ["Second context"]
        }
        namespace = {
            "OpenAI": self.make_client,
            "os": os,
            "results": {"text": ["First context"]},
            "query": "Notebook question",
            "model": MagicMock(),
            "table": table,
        }
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in request_cells:
                exec(compile(cell, "RAG_with_MiniMax.ipynb", "exec"), namespace)
        self.assertEqual(len(self.requests), 2)
        self.assert_request(self.requests[0], "Notebook question", "First context")
        self.assert_request(
            self.requests[1],
            "How do I create a table and add data in LanceDB?",
            "Second context",
        )


if __name__ == "__main__":
    unittest.main()
