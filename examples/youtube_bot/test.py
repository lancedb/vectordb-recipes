import os
import argparse
import lancedb
from lancedb.context import contextualize
from lancedb.embeddings import with_embeddings
from datasets import load_dataset
import openai
import pytest
import subprocess

# DOWNLOAD ==============================================================

subprocess.Popen("wget -c https://eto-public.s3.us-west-2.amazonaws.com/datasets/youtube_transcript/youtube-transcriptions_sample.jsonl", shell=True).wait()

# Testing ===========================================================

@pytest.fixture
def mock_embed_func(monkeypatch):
    def mock_api_call(*args, **kwargs):
        return {"data": [{"embedding": [0.5]} for _ in range(10)]}
    monkeypatch.setattr(openai.Embedding, 'create', mock_api_call)

@pytest.fixture
def mock_complete(monkeypatch):
    def mock_api_call(*args, **kwargs):
        return {"choices": [{"text": "test"}]}
    monkeypatch.setattr(openai.Completion, 'create', mock_api_call)

def test_main(mock_embed_func, mock_complete):
    args = argparse.Namespace(query="test", context_length=3, window_size=20, stride=4, openai_key="test", model="test")

    db = lancedb.connect("~/tmp/lancedb")
    table_name = "youtube-chatbot"
    if table_name not in db.table_names():
        data = load_dataset('jamescalam/youtube-transcriptions', split='train')
        df = (contextualize(data.to_pandas()).groupby("title").text_col("text").window(args.window_size).stride(args.stride).to_df())
        df = df.iloc[:10].reset_index(drop=True)
        print(df.shape)
        data = with_embeddings(embed_func, df, show_progress=True)
        data.to_pandas().head(1)
        tbl = db.create_table(table_name, data)
        print(f"Created LaneDB table of length: {len(tbl)}")
    else:
        tbl = db.open_table(table_name)

    load_dataset('jamescalam/youtube-transcriptions', split='train')
    emb = embed_func(args.query)[0]
    context = tbl.search(emb).limit(args.context_length).to_df()
    prompt = create_prompt(args.query, context)
    complete(prompt)
    top_match = context.iloc[0]
    print(f"Top Match: {top_match['url']}&t={top_match['start']}")
