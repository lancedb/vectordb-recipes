Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/instruct-multitask/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

# Multitask Embedding with LanceDB

## Introduction
Welcome to the world of Multitask Embedding with LanceDB! This blog post aims to provide a comprehensive guide to the new embedding model, particularly in conjunction with LanceDB – a swift and serverless vector database. By the end of this walkthrough, you'll not only grasp the fundamentals but also ponder, "Why didn't I try this before?" with the realization that it's surprisingly easy.


## Practical Applications
Now, let's delve into practical applications leveraging text similarity:

- **Search:** Evaluate the similarity between a query and a document in your database.
- **Spam Filtering:** Assess the proximity of an email to established examples of spam.
- **Content Moderation:** Measure the closeness of a social media message to recognized instances of abuse.
- **Conversational Agent:** Identify the closest examples of known intents to the user's messages.

For these tasks, pre-calculating embeddings for your targets and storing them in an indexed database is crucial.

## The InstructOR Multitask Embedding Model
Introducing the InstructOR multitask embedding model – a method that computes custom embeddings for text based on provided instructions. This model opens up possibilities for task-specific embeddings, making it more efficient for certain applications.

## Getting Hands-On with LanceDB
Now, why LanceDB? This will become clear as we proceed.

See, the above colab link for live coding and experimentation.