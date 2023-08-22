# Product Recommender using Collaborative Filtering and LanceDB

Use LanceDB and collaborative filtering to recommend products based on a user's past buying history. We used the Instacart dataset as our data for this example.
Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/product_recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

To run this example, you must first create a Kaggle account. Then, go to the 'Account' tab of your user profile and select 'Create New Token'. This will trigger the download of kaggle.json, a file containing your API credentials.

Add Kaggle credentials to `~/.kaggle/kaggle.json` on Linux, OSX, and other UNIX-based operating systems or `C:\Users\<Windows-username>\.kaggle\kaggle.json` for Window's users. 

### Python
Download the dataset (you must have requirements installed first!) You will need to accept the rules of the `instacart-market-basket-analysis` competition, which you can do so [here](https://www.kaggle.com/competitions/instacart-market-basket-analysis/rules).

```bash
kaggle competitions download -c instacart-market-basket-analysis
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
