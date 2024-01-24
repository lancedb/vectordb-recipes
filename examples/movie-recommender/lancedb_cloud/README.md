# Movie Recommender with Collaborative Filtering
![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/c6950e3e-6e76-4bf5-99a0-29e17ee1ab46)

This simple example covers how to create a LanceDB table remotely followed by basic searches. The search result is stored as a pandas Dataframe
Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/movie-recommender/lancedb_cloud/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Get dataset
Download and unzip the dataset from [MovieLens](https://grouplens.org/datasets/movielens/latest/). The example uses the 100k small dataset.
```bash
curl https://files.grouplens.org/datasets/movielens/ml-latest-small.zip -o ml-latest-small.zip
unzip ml-latest-small.zip
```

### Set credentials
if you would like to set api key through an environment variable:
```
export LANCEDB_API_KEY="sk_..."
```

replace the following lines in main.py with your project slug and api key"
```
db_url = "db://your-project-name"
    api_key="sk_..."
```

### Python
Run the script
```python
python main.py
```
