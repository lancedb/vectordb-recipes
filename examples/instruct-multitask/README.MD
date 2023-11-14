<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/instruct-multitask/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

# Multitask Embedding with LanceDB
We are integrating the Instruct Embedding Model to our embedding API which will reduce redundant code structure and overhead. \
Find more about the Instruct Multitask Model [here](https://instructor-embedding.github.io/).


## Practical Applications

- **Search:** Evaluate the similarity between a query and a document in your database.
- **Spam Filtering:** Assess the proximity of an email to established examples of spam.
- **Content Moderation:** Measure the closeness of a social media message to recognized instances of abuse.
- **Conversational Agent:** Identify the closest examples of known intents to the user's messages.


## Getting Hands-On with LanceDB
See, the above colab link for live coding and experimentation.

## For using the python file, make sure to first install LanceDB this way.

```bash
pip install git+https://github.com/lancedb/lancedb.git@main#subdirectory=python
```
Install other dependecies from requirements.txt file of this folder.

