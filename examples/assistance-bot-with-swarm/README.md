# Assistant bot with OpenAI's Swarm

This example shows a customer service bot that has two parts: one for interacting with users and another for providing help. It includes tools to assist in these tasks. The `run_demo_loop` function helps us create an interactive demo session.

## Overview

The support bot has two main parts:

1. **User Interface Agent**: This part interacts with users at first and directs them to the help center based on what they need.
2. **Help Center Agent**: This part offers detailed help and support using various tools and is connected to a LanceDB VectorDB to retrieve documents.

## Setup

To start the bot:

set OpenAI key as env variable
```
export OPENAI_API_KEY="sk-yourapikey"
```

1. **Install requirements**

```python3  
    pip install -r requirements.txt
    git+ssh://git@github.com/openai/swarm.git
```

2. **Prepare and Ingest dataset in LanceDB**

We'll prepare dataset from OpenAI in JSON format and ingest it in LanceDB table.
```python3
    python3 dataset_prep.py
```

3. **Ready to RUN**

Now you are ready to run assistant bot with Swarm
```python3
python3 main.py
```

*Note: You can change dataset and ingestion pipeline accordingly for your dataset to build agents around it.*

