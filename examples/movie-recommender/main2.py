import lancedb

import numpy as np
import pandas as pd
import tensorflow as tf
from keras import layers
from sklearn.calibration import LabelEncoder

ratings = pd.read_csv('./ml-latest-small/ratings.csv', header=None, names=["user id", "movie id", "rating", "timestamp"])
ratings = ratings.iloc[1:, :]

movies = pd.read_csv('./ml-latest-small/movies.csv', header=None, names=["movie id", "title", "genres"])
movies = movies.iloc[1:, :]
movies = movies[['movie id', 'title']]

merged = pd.merge(ratings, movies, how="inner", on="movie id")
merged['rating'] = pd.to_numeric(merged['rating'], downcast='float')
print(merged.head())

refined = merged.groupby(by=['user id', 'title'], as_index=False).agg({'rating': 'mean'})
print(refined.head())


user_enc = LabelEncoder()
refined['user'] = user_enc.fit_transform(refined['user id'].values)
n_users = refined['user'].nunique()

item_enc = LabelEncoder()
refined['movie'] = item_enc.fit_transform(refined['title'].values)
n_movies = refined['movie'].nunique()

print(refined.head())

min_rating = min(refined['rating'])
max_rating = max(refined['rating'])

print(">>> n_users: ", n_users, "n_movies: ", n_movies, "min_rating: ", min_rating, "max_rating: ", max_rating)

x = refined[['user', 'movie']].values
y = refined['rating'].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
i = int(0.9 * refined.shape[0])
x_train, x_test, y_train, y_test = (
    x[:i],
    x[i:],
    y[:i],
    y[i:],
)


print(">>> x_train:", x_train.shape, "x_test:", x_test.shape, "y_train:", y_train.shape, "y_test:", y_test.shape)

x_train_array = [x_train[:, 0], x_train[:, 1]]
x_test_array = [x_test[:, 0], x_test[:, 1]]



try:
    model = tf.keras.models.load_model('./trained_model2')
    print("loaded model: " + str(model.summary()))
except:
    output_dim = 120

    user = layers.Input(shape = (1,))
    u = layers.Embedding(n_users, output_dim, embeddings_initializer = 'he_normal', embeddings_regularizer = tf.keras.regularizers.l2(1e-6))(user)
    u = layers.Reshape((output_dim,))(u)

    movie = layers.Input(shape = (1,))
    m = layers.Embedding(n_movies, output_dim, embeddings_initializer = 'he_normal', embeddings_regularizer = tf.keras.regularizers.l2(1e-6))(movie)
    m = layers.Reshape((output_dim,))(m)

    x = layers.Concatenate()([u, m])
    x = layers.Dropout(0.05)(x)

    x = layers.Dense(32, kernel_initializer = 'he_normal')(x)
    x = layers.Activation(activation='relu')(x)
    x = layers.Dropout(0.05)(x)

    x = layers.Dense(16, kernel_initializer='he_normal')(x)
    x = layers.Activation(activation='relu')(x)
    x = layers.Dropout(0.05)(x)

    x = layers.Dense(9)(x)
    x = layers.Activation(activation='softmax')(x)

    model = tf.keras.models.Model(inputs=[user, movie], outputs=x)
    model.compile(optimizer='sgd', loss=tf.keras.losses.SparseCategoricalCrossentropy(), metrics=['accuracy'])
    print(model.summary())

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.75, patience=3, min_lr=0.000001, verbose=1)

    history = model.fit(
        x=x_train_array,
        y=y_train,
        batch_size=128,
        epochs=50,
        verbose=1,
        validation_data=(x_test_array, y_test),
        shuffle=True,
        callbacks=[reduce_lr]
    )

    model.save('./trained_model2')



def get_embeddings(user_id):
    enc_user_id = user_enc.transform([user_id])
    seen_movies = list(refined[refined['user id'] == user_id]['movie'])
    unseen_movies = [i for i in range(min(refined['movie']), max(refined['movie']) + 1) if i not in seen_movies]
    input = [np.asarray(list(enc_user_id) * len(unseen_movies)), np.asarray(unseen_movies)]
    embedding = model.predict(input)
    return embedding

embeddings = []
titles = []

i = int(input())

# for i in range(3, 4):
emb = get_embeddings(str(i))
emb = np.max(emb, axis=1)
temp = np.argsort(emb)[::-1]
temp = item_enc.inverse_transform(temp)
embeddings.append(emb)
titles.append(temp)


print(embeddings)
print(titles)
