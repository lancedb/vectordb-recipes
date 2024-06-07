# LlamaIndex and LanceDB Cloud Demo

In this demo, we are going to show how to use LanceDB Cloud to perform vector searches in LlamaIndex


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
OPENAI_API_KEY=... python main.py
```