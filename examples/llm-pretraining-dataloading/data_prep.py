# Process the dataset and write it to the disk as a lance dataset to be read in later
import lance
import pyarrow as pa
from datasets import load_dataset
from tqdm.auto import tqdm
from transformers import GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

print("Downloading the dataset...")
dataset = load_dataset("roneneldan/TinyStories", data_files={'train': 'TinyStoriesV2-GPT4-train.txt'})

print("Tokenizing the dataset and writing it as a lance dataset...")
# Join 'total_rows' number of sentences one after another
all_tokens = []
# Only choosing 1K sentences for now. Increase if you want to train it for longer on larger hardware
total_rows = 100_000_000
data = dataset['train'].select([x for x in range(total_rows)])
for row in tqdm(data['text'], total=len(data)):
    row = row.replace("<|endoftext|>", " ")
    encoded = tokenizer(row)['input_ids']
    all_tokens.extend(encoded)

pa_table = pa.Table.from_arrays([all_tokens], names=['value'])
lance.write_dataset(pa_table, "tiny_stories_gpt4_encoded.lance", {'model': 'create'})

print(f"Total tokens in tokenized dataset: {len(all_tokens):,.0f}")

print("Dataset tokenized and save at tiny_stories_gpt4_encoded.lance")