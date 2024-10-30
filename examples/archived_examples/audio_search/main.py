from datasets import load_dataset
from panns_inference import AudioTagging
from tqdm import tqdm
from IPython.display import Audio, display
import numpy as np
import lancedb


def create_audio_embedding(audio_data):
    return at.inference(audio_data)


def insert_audio():
    batches = [batch["audio"] for batch in dataset.iter(100)]
    meta_batches = [batch["category"] for batch in dataset.iter(100)]
    audio_data = [np.array([audio["array"] for audio in batch]) for batch in batches]
    meta_data = [np.array([meta for meta in batch]) for batch in meta_batches]
    for i in tqdm(range(len(audio_data))):
        (_, embedding) = create_audio_embedding(audio_data[i])
        data = [
            {
                "audio": x[0]["array"],
                "vector": x[1],
                "sampling_rate": x[0]["sampling_rate"],
                "category": x[2],
            }
            for x in zip(batches[i], embedding, meta_data[i])
        ]
        if table_name not in db.table_names():
            tbl = db.create_table(table_name, data)
        else:
            tbl = db.open_table(table_name)
            tbl.add(data)


def search_audio(id):
    tbl = db.open_table(table_name)
    audio = dataset[id]["audio"]["array"]
    category = dataset[id]["category"]
    display(Audio(audio, rate=dataset[id]["audio"]["sampling_rate"]))
    print("Category:", category)

    (_, embedding) = create_audio_embedding(audio[None, :])
    result = tbl.search(embedding[0]).limit(5).to_df()
    print(result)
    for i in range(len(result)):
        display(Audio(result["audio"][i], rate=result["sampling_rate"][i]))
        print("Category:", result["category"][i])


if __name__ == "__main__":
    global dataset, at, db, table_name

    dataset = load_dataset("ashraq/esc50", split="train")
    at = AudioTagging(checkpoint_path=None, device="cuda")

    db = lancedb.connect("data/audio-lancedb")
    table_name = "audio-search"

    # This function will take a while to run
    # Run if you don't have the LanceDB table yet, but skip if you already have it
    insert_audio()

    # The audio won't display in command line, but it will display in Jupyter Notebook
    search_audio(500)
