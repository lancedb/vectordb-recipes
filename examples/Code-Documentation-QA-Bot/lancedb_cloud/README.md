# Code documentation Q&A bot example with LangChain

![imgonline-com-ua-twotoone-RaRlTe66ft3RUvK](https://github.com/lancedb/vectordb-recipes/assets/15766192/4682b39d-62f4-4722-bc64-f45d45ec8a22)


This Q&A bot will allow you to query your own documentation easily using questions. We'll also demonstrate the use of LangChain and LanceDB Cloud using the OpenAI API. In this example we'll use **Numpy 1.26** documentation, but, this could be replaced for your own docs as well.
Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Code-Documentation-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>


### Set credentials
if you would like to set api key through an environment variable:
```
export LANCEDB_API_KEY="sk_..."
```
or
```
import os
import getpass

os.environ["LANCEDB_API_KEY"] = getpass.getpass("Enter Your LANCEDB API Key:")
```

replace the following lines in main.py with your project slug and api key"
```
db_url="db://your-project-slug-name"
api_key="sk_..."
region="us-east-1"
```

### Run the script
```python
OPENAI_API_KEY=... python main.py --query "what is a vectordb?"
```

### Javascript
Run the script
```javascript
OPENAI_API_KEY=... node index.js
```