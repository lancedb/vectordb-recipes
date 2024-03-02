import lancedb
import glob
import re

import yt_dlp
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast

# Set options for youtube_dl
ydl_opts = {
    "retries": 0,
    "quiet": True,  # Silence youtube_dl output
    "extract_flat": True,  # Extract metadata only, no download
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


def embed_func(query):
    inputs = TOKENIZER([query], truncation=True, padding=True, return_tensors="pt")
    text_features = MODEL.get_text_features(**inputs)
    return text_features.detach().numpy()[0]


def get_video_title(video_id):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=False
            )
            return info.get("title", None)
        except yt_dlp.utils.DownloadError:
            return None


db = lancedb.connect("data/video-lancedb")

setup_clip_model("openai/clip-vit-base-patch32")
videos = list(
    set(
        [
            re.search("(?<=videos\/).*(?=\/)", name).group()
            for name in glob.glob("./videos/*/**")
        ]
    )
)


def insert(video_ids):
    titles = [(vid, get_video_title(vid)) for vid in video_ids]
    titles = [t for t in titles if t[1] is not None]
    video_ids, titles = zip(*titles)
    text_features = [embed_func(title) for title in titles]
    if "videos" in db.table_names():
        table = db.open_table("videos")
        table.add(
            [
                {"vector": im, "text": title, "video_id": vid, "start_time": 0}
                for (im, vid, title) in zip(text_features, video_ids, titles)
            ]
        )
    else:
        db.create_table(
            "videos",
            [
                {"vector": im, "text": title, "video_id": vid, "start_time": 0}
                for (im, vid, title) in zip(text_features, video_ids, titles)
            ],
        )
    print("done")


import concurrent.futures


def threaded_video_processing(videos, chunk_size, max_workers):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(videos), chunk_size):
            chunk = videos[i : i + chunk_size]
            executor.submit(insert, chunk)


# Assuming you have defined the insert function and videos list

chunk_size = 500  # Number of videos to process in each chunk
max_workers = 5  # Number of concurrent threads

threaded_video_processing(videos, chunk_size, max_workers)
