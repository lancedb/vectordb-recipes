from datasets import load_dataset
from enum import Enum
import lancedb
from tqdm import tqdm
from IPython.display import display
import clip
import torch


class Animal(Enum):
    italian_greyhound = 0
    coyote = 1
    beagle = 2
    rottweiler = 3
    hyena = 4
    greater_swiss_mountain_dog = 5
    Triceratops = 6
    french_bulldog = 7
    red_wolf = 8
    egyption_cat = 9
    chihuahua = 10
    irish_terrier = 11
    tiger_cat = 12
    white_wolf = 13
    timber_wolf = 14


def embed(img):
    image = preprocess(img).unsqueeze(0).to(device)
    embs = model.encode_image(image)
    return embs.detach().numpy()[0].tolist()


def image_search(id):
    print("\n----- Image Search -----\n")
    print(Animal(test[id]["labels"]).name)
    display(test[id]["img"])

    res = tbl.search(embed(test[id]["img"])).limit(5).to_df()
    print(res)
    for i in range(5):
        print(Animal(res["label"][i]).name)
        data_id = int(res["id"][i])
        display(dataset[data_id]["img"])


def embed_txt(txt):
    text = clip.tokenize([txt]).to(device)
    embs = model.encode_text(text)
    return embs.detach().numpy()[0].tolist()


def text_search(text):
    print("\n----- Text Search -----\n")
    res = tbl.search(embed_txt(text)).limit(5).to_df()
    print(res)
    for i in range(len(res)):
        print(Animal(res["label"][i]).name)
        data_id = int(res["id"][i])
        display(dataset[data_id]["img"])


def create_data(db):
    tbl = db.create_table(
        "animal_images",
        [{"vector": embed(dataset[0]["img"]), "id": 0, "label": dataset[0]["labels"]}],
    )

    data = []
    for i in tqdm(range(1, len(dataset))):
        data.append(
            {"vector": dataset[i]["img"], "id": i, "label": dataset[i]["labels"]}
        )

    batched_data = [data[n : n + 50] for n in range(0, len(data), 50)]

    for i in tqdm(batched_data):
        batch_data = []
        for j in i:
            row = {}
            row["vector"] = embed(j["vector"])
            row["id"] = j["id"]
            row["label"] = j["label"]
            batch_data.append(row)
        tbl.add(batch_data)

    return tbl


if __name__ == "__main__":
    global dataset
    dataset = load_dataset(
        "CVdatasets/ImageNet15_animals_unbalanced_aug1", split="train"
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    global model, preprocess
    model, preprocess = clip.load("ViT-B/32", device=device)

    db = lancedb.connect("./data/tables")

    # This function will take ~10 minutes, run if you don't have the data yet
    # tbl = create_data(db)

    # Run this to open the table for future runs
    tbl = db.open_table("animal_images")
    print(tbl.to_pandas())

    global test
    test = load_dataset(
        "CVdatasets/ImageNet15_animals_unbalanced_aug1", split="validation"
    )

    image_search(0)
    text_search("a full white dog")
