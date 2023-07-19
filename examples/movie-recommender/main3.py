import lancedb

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import layers
from sklearn.calibration import LabelEncoder
from tqdm import tqdm

#pd.set_option('display.max_columns', None)


movies = pd.read_csv('./ml-latest-small/movies.csv', header=None, names=["movie id", "title", "genres"])
movies = movies.iloc[1:, :]
movies = movies.drop_duplicates(subset=['title'])

genres = movies['genres'].str.split('|', expand=True)
movies = movies[['movie id', 'title']]

for i, row in tqdm(genres.iterrows(), total=genres.shape[0]):
    for j in range(10):
        if str(row[j]) not in movies.columns:
            movies[str(row[j])] = 0
        if row[j] is not None:
            movies.loc[i, str(row[j])] = 1

movies = movies.drop(columns=['None'])


links = pd.read_csv('./ml-latest-small/links.csv', header=None, names=["movie id", "imdb id", "tmdb id"])
links = links.iloc[1:, :]

movies = pd.merge(links, movies, how="inner", on="movie id")
print(movies)

item_enc = LabelEncoder()
movies['movie'] = item_enc.fit_transform(movies['title'].values)
n_movies = movies['movie'].nunique()

x = movies[['movie']].values
y = movies[['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Mystery', 'Sci-Fi', 'War', 'Musical', 'Documentary', 'IMAX', 'Western', 'Film-Noir', '(no genres listed)']].values

try:
    model = tf.keras.models.load_model('./trained_model3')
    print("loaded model: " + str(model.summary()))
except:

    model = tf.keras.Sequential()
    model.add(layers.Embedding(n_movies, 32, input_length=1, name="embedding"))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(20, activation='sigmoid'))
    model.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), metrics=['accuracy'])

    history = model.fit(
        x=x,
        y=y,
        batch_size=64,
        epochs=100,
        verbose=1,
        shuffle=True,
    )

    model.save('./trained_model3')


emb = model.get_layer('embedding')
emb = emb.get_weights()

data_df = pd.DataFrame()
data_df['title'] = movies['title']
data_df['vector'] = emb[0].tolist()
data_df['imdb_id'] = movies['imdb id']
data_df.reset_index(drop=True, inplace=True)
genre_list = genres.apply(lambda x: ','.join(x.dropna().astype(str)), axis=1)
genre_list = genre_list.rename('genres')
genre_list.reset_index(drop=True, inplace=True)
data_df = pd.concat([data_df, genre_list], axis=1)
print(data_df)

db = lancedb.connect("/data/test-db")

try:
    table = db.create_table("movie_embeddings", data=data_df)
except:
    table = db.open_table("movie_embeddings")

def get_similar_movies(title):
    vectors = data_df[data_df.title == title].vector.values[0]
    results = table.search(vectors).limit(10).to_df()
    return results

print(get_similar_movies("Avengers, The (1998)"))