import argparse
import io
import PIL
import duckdb
import lancedb
import lance
import pyarrow.compute as pc
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast
import gradio as gr
import pytest
import subprocess
from main import create_table, setup_clip_model, find_image_vectors, find_image_keywords, find_image_sql, embed_func, create_gradio_dash, _extract

# DOWNLOAD ==============================================================

subprocess.Popen("wget https://eto-public.s3.us-west-2.amazonaws.com/datasets/diffusiondb_lance.tar.gz", shell=True).wait()
subprocess.Popen("tar -xvf diffusiondb_lance.tar.gz", shell=True).wait()
subprocess.Popen("mv diffusiondb_test rawdata.lance", shell=True).wait()

# TESTING ==============================================================

def test_main():
    args = argparse.Namespace(model_id="openai/clip-vit-base-patch32", dataset="rawdata.lance")
    setup_clip_model(args.model_id)
    global tbl
    tbl = create_table(args.dataset)
    create_gradio_dash()