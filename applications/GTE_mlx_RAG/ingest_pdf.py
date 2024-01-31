import argparse

import pandas as pd
from unstructured.partition.pdf import partition_pdf

import lancedb.embeddings.gte
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector


def split_text_into_chunks(text, chunk_size, overlap):
    """
    Split text into chunks with a specified size and overlap.

    Parameters:
    - text (str): The input text to be split into chunks.
    - chunk_size (int): The size of each chunk.
    - overlap (int): The number of characters to overlap between consecutive chunks.

    Returns:
    - List of chunks (str).
    """
    if chunk_size <= 0 or overlap < 0:
        raise ValueError("Invalid chunk size or overlap value.")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def pdf_to_lancedb(pdf_file: str, path: str = "/tmp/lancedb"):
    """
    create lancedb table from a pdf file

    Parameters:
    - pdf_file (str): The path to the input PDF file.
    - vdb_file (str): The path to store the vector DB.
                      default: /tmp/lancedb

    Returns:
    - None
    """
    elements = partition_pdf(pdf_file)
    content = "\n\n".join([e.text for e in elements])

    chunks = split_text_into_chunks(text=content, chunk_size=1000, overlap=200)

    model = (
        get_registry().get("gte-text").create(mlx=True)
    )  # mlx=True for Apple silicon only.

    class TextModel(LanceModel):
        text: str = model.SourceField()
        vector: Vector(model.ndims()) = model.VectorField()

    df = pd.DataFrame({"text": chunks})
    db = lancedb.connect(path)
    tbl = db.create_table("test", schema=TextModel, mode="overwrite")
    tbl.add(df)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Vector DB from a PDF file")
    # Input
    parser.add_argument(
        "--pdf",
        help="The path to the input PDF file",
        default="flash_attention.pdf",
    )
    # Output
    parser.add_argument(
        "--db_path",
        type=str,
        default="/tmp/lancedb",
        help="The path to store the vector DB",
    )
    args = parser.parse_args()
    pdf_to_lancedb(args.pdf, args.db_path)
    print("ingestion done , move to query!")
