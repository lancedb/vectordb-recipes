import nltk
import pandas as pd

nltk.download("punkt")
import re
import os
import ollama

# lancedb modules for embedding api
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


# model definition using LanceDB Embedding API
model1 = get_registry().get("openai").create()
model2 = get_registry().get("ollama").create(name="llama3")
model3 = get_registry().get("ollama").create(name="mistral")


# define schema for Embedding Spaces with embedding api
class TextModel1(LanceModel):
    text: str = model1.SourceField()
    vector: Vector(model1.ndims()) = model1.VectorField()


class TextModel2(LanceModel):
    text: str = model2.SourceField()
    vector: Vector(model2.ndims()) = model2.VectorField()


class TextModel3(LanceModel):
    text: str = model3.SourceField()
    vector: Vector(model3.ndims()) = model3.VectorField()


# Embedding Spaces
def LanceDBEmbeddingSpace(df):
    """
    Create 3 Embedding spaces with Colbert, Llama3 and Mistral
    """
    db = lancedb.connect("/tmp/lancedb")

    print("Embedding spaces creation started \U0001F6A7.....")
    table1 = db.create_table(
        "embed_space1",
        schema=TextModel1,
        mode="overwrite",
    )

    table2 = db.create_table(
        "embed_space2",
        schema=TextModel2,
        mode="overwrite",
    )

    table3 = db.create_table(
        "embed_space3",
        schema=TextModel3,
        mode="overwrite",
    )

    table1.add(df)
    table2.add(df)
    table3.add(df)

    print("3 Embedding spaces created \U0001f44d")
    return table1, table2, table3


if __name__ == "__main__":
    filename = input(
        "Enter filepath(.txt), you want to query(Default file: lease.txt) : "
    )

    if filename == "":
        filename = "lease.txt"
    else:
        if not os.path.exists(filename):
            print("Given ", filename, " doesn't exists \U0000274c")
            exit()
    # Read Document
    with open(filename, "r") as file:
        text_data = file.read()

    # Split the text using the recursive character text splitter
    chunks = recursive_text_splitter(text_data, max_chunk_length=100, overlap=10)
    df = pd.DataFrame({"text": chunks})
    table1, table2, table3 = LanceDBEmbeddingSpace(df)

    # Query  Question
    while True:
        question = input("Enter Query: ")
        if question in ["q", "exit", "quit"]:
            break

        # Query Search
        print("Query Search started ......")
        result1 = table1.search(question).limit(3).to_list()
        result2 = table2.search(question).limit(3).to_list()
        result3 = table3.search(question).limit(3).to_list()

        context = (
            [r["text"] for r in result1]
            + [r["text"] for r in result2]
            + [r["text"] for r in result3]
        )
        print("Answer generation started ....")

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

        print("Answer: ", response["message"]["content"])
