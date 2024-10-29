import pandas as pd
import lancedb
from lancedb.pydantic import LanceModel, Vector
from lancedb.embeddings import get_registry

from datasets import load_dataset

EMBEDDING_MODEL = "text-embedding-ada-002"

# load dataset
dataset_name = 'Prasant/openai-dataset'
dataset = load_dataset(dataset_name)
article_df = pd.DataFrame(dataset['train'])

# ingest data inside table
db = lancedb.connect("/tmp/db")
func = get_registry().get("openai").create(name=EMBEDDING_MODEL)


class Article(LanceModel):
    text: str = func.SourceField()
    vector: Vector(func.ndims()) = func.VectorField()
    title: str
    url: str


table = db.create_table("help-center", schema=Article, mode="overwrite")

table.add(article_df)

print(len(table))
