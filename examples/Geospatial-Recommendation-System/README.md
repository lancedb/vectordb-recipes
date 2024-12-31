# Geospatial Recommendation System

In this tutorial, we'll enhance our restaurant recommendation system using Full Text Search (FTS) Indexes and Geospatial APIs.

1. Extract User Preferences: Identify key details from user input such as preferred cuisines and location.
2. Construct Query String: Synthesize these details into a structured query string for searching.
3. Perform FTS Index Search: Use the query string to find relevant restaurant recommendations.
4. Apply Geospatial Filtering: Use a Geospatial API to locate the user and refine recommendations based on proximity.

We can enhance later on by adding a filter to sort the recommendations based on distance

## Setup Instructions

1. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required packages:
   ```bash
   pip install lancedb pandas sentence-transformers requests
   ```

2. **Prepare Data**:
   Place your restaurant data CSV file in the `data.csv` format in the project directory.

3. **Run the Notebook**:
   Open the `geospatial-recommendation.ipynb` notebook in Jupyter or Google Colab and execute the cells sequentially.

## Learn More: Blog

For a detailed explanation of GraphRAG check out our blog post:

[Read the Blog Post](https://blog.lancedb.com/geospatial-restaurant-recommendation-system/)

## Experimentation and Source Code

To explore and run experiments with both GraphRAG and traditional RAG, access the source code and experiment setup in the provided Colab notebook:

Run Experiments in Google Colab

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Geospatial-Recommendation-System/geospatial-recommendation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
