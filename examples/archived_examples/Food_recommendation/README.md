# Food Recommendation System

## Overview

This project is a vector-based food recommendation system utilizing LanceDB for full-text search (FTS), hybrid search, and vector search. It integrates the  reranker model to enhance search results and provide accurate food recommendations.

## Features

- **Vector-Based Recommendations**: Utilizes advanced vector search to find similar food items.
- **Full-Text Search (FTS)**: Enables efficient searching of food items based on text descriptions.
- **Hybrid Search**: Combines both vector search and full-text search for comprehensive results.
- **Jina Reranker Model**: Improves search result accuracy by reranking models. 

## Setup

To set up the project, follow these steps:

1. **Install Dependencies**:
   ```sh
   !pip install pandas lancedb
   ```

2. **Run the Colab Notebook**: Use the provided Colab link to interact with the recommendation system.
 
   <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/food_recommandation/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>


## Usage


##### Download data from  https://www.kaggle.com/datasets/schemersays/food-recommendation-system

1. **Data Preparation**:

   - Include important columns (e.g., food name, type, rating) into the `text` column for better FTS and search performance.
   - Add both numerical and string representations of ratings to improve accuracy.

3. **Query the System**:
   - Ask about favorite food items and specify rating types.
   - The system will provide recommendations based on the given preferences.


## Additional Resources

- **LanceDB Documentation**: [LanceDB Docs](https://lancedb.github.io/lancedb/)
