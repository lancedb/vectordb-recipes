import json
import os

import pandas as pd
import lancedb

EMBEDDING_MODEL = "text-embedding-ada-002"

article_list = os.listdir("data")

articles = []

for x in article_list:
    article_path = "data/" + x

    # Opening JSON file
    f = open(article_path)
    data = json.load(f)
    articles.append(data)

    # Closing file
    f.close()

# ingest data inside table
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

db = lancedb.connect("/tmp/db")
func = get_registry().get("openai").create(name=EMBEDDING_MODEL)


class Article(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
    title: str
    url: str


table = db.create_table("help-center", schema=Article, mode="overwrite")

article_df = pd.DataFrame(articles)
table.add(article_df)

print(len(table))
