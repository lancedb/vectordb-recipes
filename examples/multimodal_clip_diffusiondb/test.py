import argparse
import subprocess
from main import (
    create_table,
    setup_clip_model,
    create_gradio_dash,
)

# DOWNLOAD ==============================================================

subprocess.Popen(
    "wget https://eto-public.s3.us-west-2.amazonaws.com/datasets/diffusiondb_lance.tar.gz",
    shell=True,
).wait()
subprocess.Popen("tar -xvf diffusiondb_lance.tar.gz", shell=True).wait()
subprocess.Popen("mv diffusiondb_test rawdata.lance", shell=True).wait()

# TESTING ==============================================================


def test_main():
    args = argparse.Namespace(
        model_id="openai/clip-vit-base-patch32", dataset="rawdata.lance"
    )
    setup_clip_model(args.model_id)
    global tbl
    tbl = create_table(args.dataset)
    create_gradio_dash()
