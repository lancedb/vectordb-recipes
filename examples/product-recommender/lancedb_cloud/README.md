# Product Recommender using Collaborative Filtering and LanceDB

Use LanceDB and collaborative filtering to recommend products based on a user's past buying history. We used the Instacart dataset as our data for this example.
Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/product-recommender/lancedb_cloud/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Get dataset
To run this example, please download the dataset from our s3 bucket: http://vectordb-recipes.s3.us-west-2.amazonaws.com/product-recommender.zip
!!!This example needs to be run on GPU otherwise it will be very slow. 
It covers how to create a LanceDB table remotely, how to create an index on the vector column to accelerate search, followed by search on the remote table where results are saved as a pandas Dataframe.

```
wget http://vectordb-recipes.s3.us-west-2.amazonaws.com/product-recommender.zip
unzip product-recommender.zip
cp product-recommender/*.zip .
rm -fr product-recommender
```

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

Run the script 
```python
python main.py
```

| Argument | Default Value | Description |
|---|---|---|
| factors | 100 | dimension of latent factor vectors |
| regularization | 0.05 | strength of penalty term |
| iterations | 50 | number of iterations to update |
| num-threads | 1 | amount of parallelization |
| num-partitions | 256 | number of partitions of the index |
| num-sub-vectors | 16 | number of sub-vectors (M) that will be created during Product Quantization (PQ) |
