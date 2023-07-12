# Code documentation Q&A bot example with LangChain

![imgonline-com-ua-twotoone-WTf6rm7OMX](https://github.com/lancedb/vectordb-recipes/assets/15766192/0b2c1352-c2f9-4cc3-bcbb-07dcab06370b)


This Q&A bot will allow you to query your own documentation easily using questions. We'll also demonstrate the use of LangChain and LanceDB using the OpenAI API. In this example we'll use Pandas 2.0 documentation, but, this could be replaced for your own docs as well.
Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Code-Documentation-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Python
Run the script 
```python
OPENAI_API_KEY=... python main.py --query "what is a vectordb?"
```
default query = `What are the major differences in pandas 2.0?`

| Argument | Default Value | Description |
|---|---|---|
| query | "What are the major ..." | query to search |
| openai-key | | OpenAI API Key, not required if `OPENAI_API_KEY` env var is set  |

### Javascript
Run the script
```javascript
OPENAI_API_KEY=... node index.js
```
