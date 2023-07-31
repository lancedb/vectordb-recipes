from datasets import load_dataset
from panns_inference import AudioTagging
import numpy as np

dataset = load_dataset("ashraq/esc50", split="train")
at = AudioTagging(checkpoint_path=None, device="cpu")
print("hi")

import lancedb
db = lancedb.connect("data/audio-lancedb")
table_name = "audio-search"
batches = [batch["audio"] for batch in dataset.iter(100)]
audio_data = [np.array([audio["array"] for audio in batch]) for batch in batches]
for i in range(audio_data.length):  
    (clipwise_output, embedding) = at.inference(audio_data[i])
    data = [{"audio": a, "vector": e} for (a,e), in zip(batches[i], embedding)]
    if table_name not in db.table_names():
        tbl = db.create_table(table_name, data)
    else:
        tbl = db.open_table(table_name)
        tbl.add(data)