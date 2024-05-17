import nltk
import pandas as pd

nltk.download("punkt")
import re
import ollama

# lancedb imports for embedding api
import lancedb
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector


# Recursive Text Splitter
def recursive_text_splitter(text, max_chunk_length=1000, overlap=100):
    """
    Helper function for chunking text recursively
    """
    # Initialize result
    result = []

    current_chunk_count = 0
    separator = ["\n", " "]
    _splits = re.split(f"({separator})", text)
    splits = [_splits[i] + _splits[i + 1] for i in range(1, len(_splits), 2)]

    for i in range(len(splits)):
        if current_chunk_count != 0:
            chunk = "".join(
                splits[
                    current_chunk_count
                    - overlap : current_chunk_count
                    + max_chunk_length
                ]
            )
        else:
            chunk = "".join(splits[0:max_chunk_length])

        if len(chunk) > 0:
            result.append("".join(chunk))
        current_chunk_count += max_chunk_length

    return result


# define schema for table with embedding api

model = get_registry().get("colbert").create(name="colbert-ir/colbertv2.0")


class TextModel(LanceModel):
    text: str = model.SourceField()
    vector: Vector(model.ndims()) = model.VectorField()


# add in vector db
def lanceDBConnection(df):
    """
    LanceDB insertion
    """
    db = lancedb.connect("/tmp/lancedb")
    table = db.create_table(
        "scratch",
        schema=TextModel,
        mode="overwrite",
    )
    table.add(df)
    return table


# Read Document
with open("lease.txt", "r") as file:
    text_data = file.read()

# Split the text using the recursive character text splitter
chunks = recursive_text_splitter(text_data, max_chunk_length=100, overlap=10)
df = pd.DataFrame({"text": chunks})
table = lanceDBConnection(df)

# Query  Question
k = 5
question = "When this lease document was created?"

# Semantic Search
result = table.search(question).limit(5).to_list()
context = [r["text"] for r in result]

# Context Prompt
base_prompt = """You are an AI assistant. Your task is to understand the user question, and provide an answer using the provided contexts. Every answer you generate should have citations in this pattern  "Answer [position].", for example: "Earth is round [1][2].," if it's relevant.
Your answers are correct, high-quality, and written by an domain expert. If the provided context does not contain the answer, simply state, "The provided context does not have the answer."

User question: {}

Contexts:
{}
"""

# llm
prompt = f"{base_prompt.format(question, context)}"

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "system",
            "content": prompt,
        },
    ],
)

print(response["message"]["content"])
