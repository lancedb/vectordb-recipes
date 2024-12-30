# Geospatial Recommendation System

This project is a geospatial recommendation system that uses LanceDB for vector-based information retrieval. It processes restaurant data, embeds relevant information using a sentence transformer, and provides recommendations based on user queries.

## Features

- **Data Processing**: Cleans and prepares restaurant data for analysis.
- **Embedding**: Uses a pre-trained sentence transformer to embed restaurant information.
- **Vector Database**: Stores embedded data in LanceDB for efficient retrieval.
- **Query Handling**: Extracts and processes user queries to find relevant recommendations.
- **Geospatial Analysis**: Calculates distances between user location and restaurant locations using Google Maps API.

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

## Code Overview

- **Data Loading and Cleaning**:
  - Loads restaurant data from a CSV file.
  - Cleans the data by removing duplicates and handling missing values.

- **Embedding**:
  - Uses `SentenceTransformer` to create embeddings for restaurant data.
  - Constructs a query string from relevant columns for each restaurant.

- **Database Operations**:
  - Connects to LanceDB and creates a table to store restaurant data and embeddings.
  - Uses Full-Text Search (FTS) for querying the database.

- **Query Processing**:
  - Extracts structured data from user queries using OpenAI's API.
  - Constructs a query string for searching the database.

- **Geospatial Analysis**:
  - Uses Google Maps API to geocode addresses and calculate distances.
  - Provides recommendations based on proximity to the user's location.

## Learn More: Blog

For a detailed explanation of GraphRAG check out our blog post:

[Read the Blog Post](https://blog.lancedb.com/create-a-restaurant-recommendation-system/)

## Experimentation and Source Code

To explore and run experiments with both GraphRAG and traditional RAG, access the source code and experiment setup in the provided Colab notebook:

Run Experiments in Google Colab

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Geospatial-Recommendation-System/geospatial-recommendation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
