# Reducing Hallucinations from AI Agents using Long-Term Memory
### Introduction to Critique-Based Contexting with OpenAI, LangChain, and LanceDB
AI agents can help simplify and automate tedious workflows. By going through this fitness trainer agent example, we'll introduce how you can reduce hallucinations from AI agents by using critique-based contexting.

Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/reducing_hallucinations_ai_agents/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

![Untitled (34)](https://github.com/lancedb/vectordb-recipes/assets/15766192/e87d5fcc-6f04-4592-b9ec-0156ee2c98df)


### Setup

Set environment variables for SerpApi and OpenAI API

```javascript
export OPENAI_API_KEY=...
export SERPAPI_API_KEY=...
```

### Python
Run the script
```python
python main.py --query "university student, loves running"
```
default query = `university student, loves running`

| Argument | Default Value | Description |
|---|---|---|
| query | "university student ..." | query to search |
| llm | `gpt-3.5-turbo-0613` | OpenAI LLM to use |
| embeddings | `text-embedding-ada-002` | OpenAI embeddings model to use |

### Javascript
Run the script
```javascript
node index.js
```
