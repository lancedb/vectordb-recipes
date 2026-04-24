# AG2 Multi-Agent RAG with LanceDB

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/AG2-Multiagent-RAG-with-LanceDB/main.ipynb)

This example demonstrates how to build a multi-agent RAG (Retrieval-Augmented Generation) system using [AG2](https://ag2.ai/) and [LanceDB](https://lancedb.github.io/lancedb/).

## What You'll Learn

- How to create an embedded LanceDB vector database (no server needed)
- How to register LanceDB search as an AG2 agent tool
- How to set up multi-agent conversations with AG2's GroupChat
- How two specialized agents (Research + Analyst) collaborate for RAG

## Architecture

```
User Query → UserProxy → GroupChat
                            ├── Research Agent (searches LanceDB)
                            └── Analyst Agent (synthesizes findings)
```

## Quick Start

```bash
pip install lancedb "ag2[openai]>=0.11.4,<1.0" sentence-transformers pandas
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key"
```

Then open the notebook in Colab or run locally with Jupyter.

## Technologies

- **[AG2](https://ag2.ai/)** — Multi-agent conversation framework (500K+ monthly PyPI downloads)
- **[LanceDB](https://lancedb.github.io/lancedb/)** — Embedded vector database (no server required)
