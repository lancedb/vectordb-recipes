from datasets import load_dataset
import numpy as np
import lancedb
import pytest
import main

# ==================== TESTING ====================


@pytest.fixture
def mock_embed(monkeypatch):
    def mock_inference(audio_data):
        return (None, [[0.5, 0.5]])

    monkeypatch.setattr(main, "create_audio_embedding", mock_inference)


def test_main(mock_embed):
    global dataset, db, table_name
    dataset = load_dataset("ashraq/esc50", split="train")

    db = lancedb.connect("data/audio-lancedb")
    table_name = "audio-search"

    main.dataset = dataset
    main.db = db
    main.table_name = table_name

    main.insert_audio()

    main.search_audio(500)
