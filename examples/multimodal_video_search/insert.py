from dotenv import load_dotenv
import os
import lancedb
import torch
from PIL import Image
import glob
import re

from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast
import concurrent.futures

# Set options for youtube_dl
ydl_opts = {
    'quiet': True,  # Silence youtube_dl output
    'extract_flat': True,  # Extract metadata only, no download
}

MODEL_ID = None
MODEL = None
TOKENIZER = None
PROCESSOR = None

def setup_clip_model(model_id):
    global MODEL_ID, MODEL, TOKENIZER, PROCESSOR
    MODEL_ID = model_id
    TOKENIZER = CLIPTokenizerFast.from_pretrained(MODEL_ID)
    MODEL = CLIPModel.from_pretrained(MODEL_ID)
    PROCESSOR = CLIPProcessor.from_pretrained(MODEL_ID)

def embed_func(image):
    inputs = PROCESSOR(images=image, padded=True, return_tensors="pt")
    text_features = MODEL.get_image_features(**inputs)
    return text_features.detach().numpy()[0]

from concurrent.futures import ThreadPoolExecutor

db = lancedb.connect("data/video-lancedb")
setup_clip_model('openai/clip-vit-base-patch32')

def insert(video_ids, frames):
    with torch.no_grad():
        image_features = [embed_func(Image.open(f'./videos/{vid}/frame-{frame}.jpg')) for (vid, frame) in zip(video_ids, frames)]
    if "videos" in db.table_names():
        table = db.open_table("videos")
        table.add([{'vector': im, 'text': '', 'video_id': vid, 'start_time': (int(frame) - 1) * 30} for (im, vid, frame) in zip(image_features, video_ids, frames)])
    else:
        db.create_table("videos", [{'vector': im, 'text': '', 'video_id': vid, 'start_time': (int(frame) - 1) * 30} for (im, vid, frame) in zip(image_features, video_ids, frames)])

videos = [(re.search('(?<=videos\/).*(?=\/)', name).group(), re.search('(?<=frame-).*(?=.jpg)', name).group()) for name in glob.glob('./videos/*/**')]
print(videos[:5])

def process_video_chunk(chunk):
    video_ids, frames = zip(*chunk)
    insert(video_ids, frames)

def threaded_video_processing(videos, chunk_size, max_workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(videos), chunk_size):
            chunk = videos[i:i+chunk_size]
            executor.submit(process_video_chunk, chunk)

# Assuming you have defined the insert function and videos list

chunk_size = 500  # Number of videos to process in each chunk
max_workers = 10   # Number of concurrent threads

threaded_video_processing(videos, chunk_size, max_workers)
