from datasets import load_dataset
import os
import lancedb
import getpass
import time
import argparse
from tqdm.auto import tqdm
from lancedb.embeddings import EmbeddingFunctionRegistry
from lancedb.pydantic import LanceModel, Vector


def main(query=None):
    if "COHERE_API_KEY" not in os.environ:
        os.environ["COHERE_API_KEY"] = getpass.getpass("Enter your Cohere API key: ")

    en = dataset = load_dataset(
        "wikipedia",
        "20220301.en",
        streaming=True,
    )
    fr = load_dataset("wikipedia", "20220301.fr", streaming=True)

    datasets = {"english": iter(en["train"]), "french": iter(fr["train"])}

    registry = EmbeddingFunctionRegistry().get_instance()
    cohere = registry.get(
        "cohere"
    ).create()  # uses multi-lingual model by default (768 dim)

    class Schema(LanceModel):
        vector: Vector(cohere.ndims()) = cohere.VectorField()
        text: str = cohere.SourceField()
        url: str
        title: str
        id: str
        lang: str

    db = lancedb.connect("~/lancedb")
    tbl = (
        db.create_table("wikipedia-cohere", schema=Schema, mode="overwrite")
        if "wikipedia-cohere" not in db
        else db.open_table("wikipedia-cohere")
    )

    # let's use cohere embeddings. Use can also set it to openai version of the table
    batch_size = 1000
    num_records = 10000
    data = []

    for i in tqdm(range(0, num_records, batch_size)):
        for lang, dataset in datasets.items():
            batch = [next(dataset) for _ in range(batch_size)]

            texts = [x["text"] for x in batch]
            ids = [f"{x['id']}-{lang}" for x in batch]
            data.extend(
                {
                    "text": x["text"],
                    "title": x["title"],
                    "url": x["url"],
                    "lang": lang,
                    "id": f"{lang}-{x['id']}",
                }
                for x in batch
            )

        # add in batches to avoid token limit
        tbl.add(data)
        data = []
        print("Added batch. Sleeping for 20 seconds to avoid rate limit")
        time.sleep(20)  # wait for 20 seconds to avoid rate limit

    if not query:
        it = iter(fr["train"])
        for i in range(5):
            next(it)
        query = next(it)

    rs = tbl.search(query["text"]).limit(3).to_list()
    print("Query: ", query["text"])
    print("Results: ", rs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="", help="Query to search")
    args = parser.parse_args()
    main(query=args.query)
