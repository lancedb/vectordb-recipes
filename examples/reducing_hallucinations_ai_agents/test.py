"""

import openai
import argparse
import lancedb
import pytest
from main import insert_critiques, retrieve_critiques

# TESTING ===========================================================
# Temporarily excluded
@pytest.fixture
def mock_embed_func(monkeypatch):
    def mock_api_call(*args, **kwargs):
        return {"data": [{"embedding": [0.1, 0.2, 0.3]}, {"embedding": [0.4, 0.5, 0.6]}]}
    monkeypatch.setattr(openai.Embedding, 'create', mock_api_call)

def test_main(mock_embed_func):
    args = argparse.Namespace(query="test", llm="test", embeddings="test")

    global db
    db = lancedb.connect("data/agent-lancedb")

    print(insert_critiques)
    print(retrieve_critiques)
"""