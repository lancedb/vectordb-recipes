import torch
import open_clip
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
import arxiv
import lancedb


def get_arxiv_df(embed_func):
    length = 30000
    results = arxiv.Search(
        query="cat:cs.AI OR cat:cs.CV OR cat:stat.ML",
        max_results=length,
        sort_by=arxiv.SortCriterion.Relevance,
        sort_order=arxiv.SortOrder.Descending,
    ).results()
    df = defaultdict(list)
    for result in tqdm(results, total=length):
        try:
            df["title"].append(result.title)
            df["summary"].append(result.summary)
            df["authors"].append(str(result.authors))
            df["url"].append(result.entry_id)
            df["vector"].append(embed_func(result.summary).tolist()[0])

        except Exception as e:
            print("error: ", e)

    return pd.DataFrame(df)


def embed_func_clip(text):
    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k"
    )
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    with torch.no_grad():
        text_features = model.encode_text(tokenizer(text))
    return text_features


def create_table(embed_func=embed_func_clip):
    db = lancedb.connect("db")
    df = get_arxiv_df(embed_func)

    tbl = db.create_table("arxiv", data=df, mode="overwrite")


def search_table(query, embed_func=embed_func_clip):
    db = lancedb.connect("db")
    tbl = db.open_table("arxiv")

    embs = embed_func(query)
    print(tbl.search(embs.tolist()[0]).limit(3).to_df()["title"])


if __name__ == "__main__":
    db = lancedb.connect("db")

    if "arxiv" not in db.table_names():
        tbl = create_table()

    search_table(
        """
    Segment Anything Model (SAM) has attracted significant attention due to its impressive zero-shot
    transfer performance and high versatility for numerous vision applications (like image editing with
    fine-grained control). Many of such applications need to be run on resource-constraint edge devices,
    like mobile phones. In this work, we aim to make SAM mobile-friendly by replacing the heavyweight
    image encoder with a lightweight one. A naive way to train such a new SAM as in the original SAM
    paper leads to unsatisfactory performance, especially when limited training sources are available. We
    find that this is mainly caused by the coupled optimization of the image encoder and mask decoder,
    motivated by which we propose decoupled distillation. Concretely, we distill the knowledge from
    the heavy image encoder (ViT-H in the original SAM) to a lightweight image encoder, which can be
    automatically compatible with the mask decoder in the original SAM. The training can be completed
    on a single GPU within less than one day, and the resulting lightweight SAM is termed MobileSAM
    which is more than 60 times smaller yet performs on par with the original SAM. For inference speed,
    With a single GPU, MobileSAM runs around 10ms per image: 8ms on the image encoder and 4ms
    on the mask decoder. With superior performance, our MobileSAM is around 5 times faster than the
    concurrent FastSAM and 7 times smaller, making it more suitable for mobile applications. Moreover,
    we show that MobileSAM can run relatively smoothly on CPU
    """
    )
