import argparse
from pprint import pprint

import pandas as pd
from mlx_lm import generate, load

import lancedb.embeddings.gte

TEMPLATE = """You are a helpful, respectful and honest assistant. Always answer as helpfully as possible using the context text provided. Your answers should only answer the question once and not have any text after the answer is done.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.

CONTEXT:

{context}

Question: {question}
Answer:
"""

if __name__ == "__main__":
    import lancedb

    parser = argparse.ArgumentParser(description="Query a vector DB")
    # Input
    parser.add_argument(
        "--question",
        help="The question that needs to be answered",
        default="what is flash attention?",
    )
    # Input
    parser.add_argument(
        "--db_path",
        type=str,
        default="/tmp/lancedb",
        help="The path to read the vector DB",
    )
    args = parser.parse_args()

    db = lancedb.connect(args.db_path)
    tbl = db.open_table("test")
    resp = tbl.search(args.question).limit(10).to_pandas()
    context = "\n".join(resp["text"].values)
    context = "\n".join(pd.Series(context.split("\n")).drop_duplicates())

    prompt = TEMPLATE.format(context=context, question=args.question)
    model, tokenizer = load("mlx-community/NeuralBeagle14-7B-4bit-mlx")
    ans = generate(model, tokenizer, prompt=prompt, verbose=False, max_tokens=512)

    pprint(ans)
