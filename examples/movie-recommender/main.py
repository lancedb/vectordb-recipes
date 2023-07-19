# https://grouplens.org/datasets/movielens/latest/

import lancedb

import pandas as pd
import numpy as np
import tensorflow as tf
import keras
from keras import layers
import model

# load user review dataset, get movie models, create embeddings, create table with data, query, return results

ratings = pd.read_csv('./ml-latest-small/ratings.csv')
ratings = ratings.dropna()

userIDs = ratings['userId'].unique().tolist()
user_encoded = {x: i for i, x in enumerate(userIDs)}

movieIDs = ratings['movieId'].unique().tolist()
movie_encoded = {x: i for i, x in enumerate(movieIDs)}
movie_encoded_inv = {i: x for i, x in enumerate(movieIDs)}

num_users = len(user_encoded)
num_movies = len(movie_encoded_inv)

ratings["rating"] = ratings["rating"].values.astype(np.float32)
min_rating = min(ratings["rating"])
max_rating = max(ratings["rating"])

print(">> num_users:", num_users, "num_movies:", num_movies, "min_rating:", min_rating, "max_rating:", max_rating)


ratings = ratings.sample(frac=1, random_state=np.random.RandomState())


# split data into train and test sets

x = ratings[["userId", "movieId"]].values
y = ratings["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values

train_indices = int(0.9 * ratings.shape[0])
x_train, x_test, y_train, y_test = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:],
)

print(">> x_train:", x_train.shape, "x_test:", x_test.shape, "y_train:", y_train.shape, "y_test:", y_test.shape)
try:
    model = keras.models.load_model('./trained_model1')
except:
    model = model.RecommenderNet(num_users + 1, num_movies + 1, 32)
    model.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=keras.optimizers.Adam(learning_rate=0.001))

    history = model.fit(
        x=x_train,
        y=y_train,
        batch_size=64,
        epochs=5,
        verbose=1,
        validation_data=(x_test, y_test)
    )

    model.save('./trained_model1')

print(model.summary())


test_loss = model.evaluate(x_test, y_test)
print('\nTest Loss: {}'.format(test_loss))
print("Testing Model with 1 user")
movie_df = pd.read_csv("./ml-latest-small/movies.csv")
user_id = "new_user"
movies_watched_by_user = ratings.sample(5)
movies_not_watched = movie_df[
    ~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)
]["movieId"]
movies_not_watched = list(
    set(movies_not_watched).intersection(set(movie_encoded.keys()))
)
movies_not_watched = [[movie_encoded.get(x)] for x in movies_not_watched]
user_movie_array = np.hstack(
    ([[0]] * len(movies_not_watched), movies_not_watched)
)
print(pd.DataFrame(user_movie_array).head())
ratings = model.predict(user_movie_array).flatten()
top_ratings_indices = ratings.argsort()[-10:][::-1]
recommended_movie_ids = [
    movie_encoded_inv.get(movies_not_watched[x][0]) for x in top_ratings_indices
]
print("Showing recommendations for user: {}".format(user_id))
print("====" * 9)
print("Movies with high ratings from user")
print("----" * 8)
top_movies_user = (
    movies_watched_by_user.sort_values(by="rating", ascending=False)
    .head(5)
    .movieId.values
)
movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
for row in movie_df_rows.itertuples():
    print(row.title, ":", row.genres)
print("----" * 8)
print("Top 10 movie recommendations")
print("----" * 8)
recommended_movies = movie_df[movie_df["movieId"].isin(recommended_movie_ids)]
for row in recommended_movies.itertuples():
    print(row.title, ":", row.genres)


"""
li = []
for filename in ['./ml-latest-small/links.csv', './ml-latest-small/movies.csv', './ml-latest-small/ratings.csv']:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)


movies = pd.concat(li, axis=0, ignore_index=True)
movies = movies.groupby(movies['movieId']).aggregate({'title': 'first', 'imdbId': 'first', 'tmdbId': 'first', 'genres': 'first', 'userId': 'first', 'rating': 'first'})
movies = movies.drop_duplicates(subset=["imdbId"])
print(movies)

batch = 64
for i in range(0, len(movies), batch):
    end = min(i + batch, len(movies))
    batch = movies.iloc[i:end]
    embedding = model.predict(batch['title']).tolist()
    metadata = batch.to_dict(orient="records")
    ids = batch['imdbId'].values.tolist()

    vector = list(zip(ids, embedding, metadata))
    print(vector)
"""