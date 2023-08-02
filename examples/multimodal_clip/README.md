# Multi-modal search using CLIP
![243051535-09c5afc5-7816-4687-bae4-f2ca194426ec](https://github.com/lancedb/vectordb-recipes/assets/15766192/799f94a1-a01d-4a5b-a627-2a733bbb4227)


Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_clip/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

### Get dataset
```bash
wget https://eto-public.s3.us-west-2.amazonaws.com/datasets/diffusiondb_lance.tar.gz
tar -xvf diffusiondb_lance.tar.gz
mv diffusiondb_test rawdata.lance
```

### Python
Run the script
```python
python main.py
```
