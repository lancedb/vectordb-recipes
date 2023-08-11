# Multimodal video search using CLIP and LanceDB
We used LanceDB to store frames every thirty seconds and the title of 13000+ videos, 5 random from each top category from the Youtube 8M dataset. 
Then, we used the CLIP model to embed frames and titles together. Here are the results.
![243051535-09c5afc5-7816-4687-bae4-f2ca194426ec](https://github.com/lancedb/vectordb-recipes/assets/15766192/799f94a1-a01d-4a5b-a627-2a733bbb4227)

This is a work in progress, we are still trying to get tantivy to run properly for keyword search.

Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_video_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Get dataset
```bash
wget https://vectordb-recipes.s3.us-west-2.amazonaws.com/multimodal_video_lance.tar.gz
tar -xvf multimodal_video_lance.tar.gz
mv multimodal_video.lance rawdata.lance
```

### Python
Run the script 
```python
python main.py
```
