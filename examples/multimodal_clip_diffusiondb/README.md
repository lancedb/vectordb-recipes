# Multi-modal search using CLIP with DiffusionDB
![gradio-demo](../../assets/gradio_clip_diffusiondb.gif)


Colab walkthrough - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_clip_diffusiondb/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

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
