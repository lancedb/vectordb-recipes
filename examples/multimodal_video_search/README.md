# Multimodal video search using CLIP and LanceDB
We used LanceDB to store frames every thirty seconds and the title of 13000+ videos, 5 random from each top category from the Youtube 8M dataset. 
Then, we used the CLIP model to embed frames and titles together. With LanceDB, we can perform embedding, keyword, and SQL search on these videos.

![lancedb video search demo](https://github.com/lancedb/vectordb-recipes/assets/43354492/17ecaa3d-ef65-4baa-8d91-168f9f1069c0)

Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_video_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Get dataset
```bash
wget https://vectordb-recipes.s3.us-west-2.amazonaws.com/multimodal_video_lance.tar.gz
tar -xvf multimodal_video_lance.tar.gz
mkdir -p data/video-lancedb
mv multimodal_video.lance data/video-lancedb/
```

### Python

Install dependencies
```bash
pip install -r requirements.txt
```

Run the script 
```python
python main.py
```

### Dataset generation

Here is how the `multimodal_video` dataset (the raw data) was generated:
1. `downloadcategoryids.sh` - Uses the YouTube8M dataset to retrieve 5 video ids from each category
2. `downloadvideos.py` - Uses youtube-dl to download the videos and take a screenshot every 30 seconds 
3. `insert.py` Uses the CLIP embedding model to embed each screenshot and insert into LanceDB
4. `insert_titles.py` We also get titles and embed them into LanceDB
5. We create a full text search index using tantivy with `tbl.create_fts_index("text")`

This dataset is available in our s3 bucket: https://vectordb-recipes.s3.us-west-2.amazonaws.com/multimodal_video_lance.tar.gz
