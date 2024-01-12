import zipfile
import numpy as np
import pandas as pd
import scipy.sparse
import torch
import implicit
from implicit import evaluation
import lancedb
import pydantic
from lancedb.pydantic import pydantic_to_schema, vector
import argparse

def products_bought_by_user_in_the_past(user_id: int, top: int = 10):

    selected = data[data.user_id == user_id].sort_values(by=['total_orders'], ascending=False)

    selected['product_name'] = selected['product_id'].map(product_entries.set_index('product_id')['product_name'])
    selected = selected[['product_id', 'product_name', 'total_orders']].reset_index(drop=True)
    if selected.shape[0] < top:
        return selected

    return selected[:top]

def args_parse():
    parser = argparse.ArgumentParser(description='Product Recommender')
    parser.add_argument('--factors', type=int, default=128, help='dimension of latent factor vectors')
    parser.add_argument('--regularization', type=float, default=0.05, help='strength of penalty term')
    parser.add_argument('--iterations', type=int, default=50, help='number of iterations to update')
    parser.add_argument('--num-threads', type=int, default=1, help='amount of parallelization')
    parser.add_argument('--num-partitions', type=int, default=256, help='number of partitions of the index')
    parser.add_argument('--num-sub-vectors', type=int, default=16, help='number of sub-vectors (M) that will be created during Product Quantization (PQ).')
    args = parser.parse_args()

    return args

files = [
    'instacart-market-basket-analysis.zip',
    'order_products__train.csv.zip',
    'order_products__prior.csv.zip',
    'products.csv.zip',
    'orders.csv.zip'
]

if __name__ == "__main__":
    args = args_parse()
    for filename in files:
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall('./')

    products = pd.read_csv('products.csv')
    orders = pd.read_csv('orders.csv')
    order_products = pd.concat([pd.read_csv('order_products__train.csv'), pd.read_csv('order_products__prior.csv')])

    customer_order_products = pd.merge(orders, order_products, how='inner',on='order_id')

    # create confidence table
    data = customer_order_products.groupby(['user_id', 'product_id'])[['order_id']].count().reset_index()
    data.columns=["user_id", "product_id", "total_orders"]
    data.product_id = data.product_id.astype('int64')

    data_new = pd.DataFrame([[data.user_id.max() + 1, 46149, 50], # user 1 orders 50 Zero Calorie Cola 
                            [data.user_id.max() + 2, 27845, 49], # user 2 orders 49 Organic Whole Milk
                            [data.user_id.max() + 2, 26604, 32] # user 2 orders 32 Organic Blackberries
                            ], columns=['user_id', 'product_id', 'total_orders'])
    data = pd.concat([data, data_new]).reset_index(drop = True)

    # extract unique user and product ids
    unique_users = list(np.sort(data.user_id.unique()))
    unique_products = list(np.sort(products.product_id.unique()))
    purchases = list(data.total_orders)

    # create zero-based index position <-> user/item ID mappings
    index_to_user = pd.Series(unique_users)

    # create reverse mappings from user/item ID to index positions
    user_to_index = pd.Series(data=index_to_user.index + 1, index=index_to_user.values)

    # create row and column for user and product ids
    users_rows = data.user_id.astype(int)
    products_cols = data.product_id.astype(int)

    # create CSR matrix
    matrix = scipy.sparse.csr_matrix((purchases, (users_rows, products_cols)), shape=(len(unique_users) + 1, len(unique_products) + 1))
    matrix.data = np.nan_to_num(matrix.data, copy=False)

    #split data into train and test splits
    train, test = evaluation.train_test_split(matrix, train_percentage=0.9)

    # initialize the recommender model
    model = implicit.als.AlternatingLeastSquares(factors=args.factors,
                                                regularization=args.regularization,
                                                iterations=args.iterations,
                                                num_threads=args.num_threads)

    alpha = 15
    train = (train * alpha).astype('double')

    # train the model on CSR matrix
    model.fit(train, show_progress = True)

    test = (test * alpha).astype('double')
    evaluation.ranking_metrics_at_k(model, train, test, K=100,
                            show_progress=True, num_threads=1)
    

    db_url = "your-project-name"
    api_key="sk_..."
    region = "us-east-1-dev"
    db = lancedb.connect(db_url, api_key=api_key, region=region)
    class ProductModel(pydantic.BaseModel):
        product_id: int
        product_name: str
        vector: vector(args.factors)
    schema = pydantic_to_schema(ProductModel)
    table_name = 'product_recommender'
    tbl = db.create_table(table_name, schema=schema)

    # Transform items into factors
    items_factors = model.item_factors
    product_entries = products[['product_id', 'product_name']].drop_duplicates()
    product_entries['product_id'] = product_entries.product_id.astype('int64')
    device = "cuda" if torch.cuda.is_available() else "cpu"
    item_embeddings = items_factors[1:].to_numpy().tolist() if device == "cuda" else items_factors[1:].tolist()
    product_entries['vector'] = item_embeddings

    tbl.add(product_entries)
    tbl.create_index(vector_column_name="vector")

    test_user_ids = [206210, 206211]
    test_user_factors = model.user_factors[user_to_index[test_user_ids]]
    
    # Query by user factors
    test_user_embeddings = test_user_factors.to_numpy().tolist() if device == "cuda" else test_user_factors.tolist()
    for embedding, id in zip(test_user_embeddings, test_user_ids):
        results = tbl.search(embedding).limit(10).to_pandas()
        print(results.drop(columns=['vector']).to_string(max_cols=None))
        print(products_bought_by_user_in_the_past(id, top=15).to_string(max_cols=None))
