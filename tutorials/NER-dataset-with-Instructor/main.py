# import libraries
import instructor
from pydantic import BaseModel
from openai import OpenAI
from lancedb.pydantic import Vector, LanceModel
import lancedb
from langchain_openai import OpenAIEmbeddings
from datasets import load_dataset


# load the dataset and convert to pandas dataframe
df = load_dataset(
    "fabiochiu/medium-articles",
    data_files="medium_articles.csv",
    split="train"
).to_pandas()

df = df.dropna().sample(20000, random_state=32)
# select first 1000 characters from each article
df["text"] = df["text"].str[:1000]
# join article title and the text
df["title_text"] = df["title"] + ". " + df["text"]


# schema for table
class UserData(LanceModel):
    vector: Vector(1536)
    entity: str
    content: str

# schema for instructor output
class structureData(BaseModel):
    entity: str

# Patch the OpenAI client
client = instructor.from_openai(OpenAI())
openai_embedding = OpenAIEmbeddings(model="text-embedding-3-small")

# connect lancedb
db = lancedb.connect("~/.lancedb")
table_name = "instructor_lancedb"
table = db.create_table(table_name, schema=UserData, mode="overwrite")

for index, row in df[:10].iterrows():
    # generate response
    structured_info = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=structureData,
        messages=[{"role": "user", "content": row["title_text"]}],
    )

    embedding = openai_embedding.embed_query(row["title_text"])
    userdata = UserData(vector=embedding, entity=structured_info.entity, content=row["title_text"])
    table.add([userdata])

# show table content
print(table.to_pandas())