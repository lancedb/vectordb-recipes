import argparse
import io
import PIL
import duckdb
import lancedb
import lance
import pyarrow.compute as pc
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast
import gradio as gr

# download s3://eto-public/datasets/diffusiondb/small_10k.lance to this uri

def embed_func(query):
    inputs = tokenizer([query], padding=True, return_tensors="pt")
    text_features = model.get_text_features(**inputs)
    return text_features.detach().numpy()[0]


def find_image_vectors(query, num_results):
    emb = embed_func(query)
    code = (
        "import lancedb\n"
        "db = lancedb.connect('~/datasets/demo')\n"
        "tbl = db.open_table('diffusiondb')\n\n"
        f"embedding = embed_func('{query}')\n"
        f"tbl.search(embedding).limit({ str(num_results) }).to_df()"
    )
    return (_extract(tbl.search(emb).limit(num_results).to_df()), code)


def find_image_keywords(query, num_results):
    code = (
        "import lancedb\n"
        "db = lancedb.connect('~/datasets/demo')\n"
        "tbl = db.open_table('diffusiondb')\n\n"
        f"tbl.search('{query}').limit({ str(num_results) }).to_df()"
    )
    return (_extract(tbl.search(query).limit(num_results).to_df()), code)


def find_image_sql(query):
    code = (
        "import lancedb\n"
        "import duckdb\n"
        "db = lancedb.connect('~/datasets/demo')\n"
        "tbl = db.open_table('diffusiondb')\n\n"
        "diffusiondb = tbl.to_lance()\n"
        f"duckdb.sql('{query}').to_df()"
    )
    diffusiondb = tbl.to_lance()
    return (_extract(duckdb.sql(query).to_df()), code)


def _extract(df):
    image_col = "image"
    return [(PIL.Image.open(io.BytesIO(row[image_col])), row["prompt"]) for _, row in df.iterrows()]

def arg_parse():
    parser = argparse.ArgumentParser(description='Multimodal Search')
    parser.add_argument('--num-results', type=int, default=9, help="Number of results per query")
    parser.add_argument('--model', type=str, default="openai/clip-vit-base-patch32", help='OpenAI API Key')
    args = parser.parse_args()

    return args
if __name__ == "__main__":
    args = arg_parse()
    
    MODEL_ID = args.model

    data = lance.dataset("~/datasets/rawdata.lance").to_table()
    db = lancedb.connect("~/datasets/demo")
    tbl = db.create_table("diffusiondb", data.filter(
        ~pc.field("prompt").is_null()))
    tbl = tbl.create_fts_index(["prompt"])

    db = lancedb.connect("~/datasets/demo")
    tbl = db.open_table("diffusiondb")

    tokenizer = CLIPTokenizerFast.from_pretrained(MODEL_ID)
    model = CLIPModel.from_pretrained(MODEL_ID)
    processor = CLIPProcessor.from_pretrained(MODEL_ID)

    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Tab("Embeddings"):
                vector_query = gr.Textbox(
                    value="portraits of a person", show_label=False)
                b1 = gr.Button("Submit")
            with gr.Tab("Keywords"):
                keyword_query = gr.Textbox(
                    value="ninja turtle", show_label=False)
                b2 = gr.Button("Submit")
            with gr.Tab("SQL"):
                sql_query = gr.Textbox(
                    value="SELECT * from diffusiondb WHERE image_nsfw >= 2 LIMIT 9", show_label=False)
                b3 = gr.Button("Submit")
        with gr.Row():
            code = gr.Code(label="Code", language="python")
        with gr.Row():
            gallery = gr.Gallery(
                    label="Found images", show_label=False, elem_id="gallery"
                ).style(columns=[3], rows=[3], object_fit="contain", height="auto")

        b1.click(find_image_vectors, inputs=[vector_query, args.num_results],
                 outputs=[gallery, code])
        b2.click(find_image_keywords, inputs=[keyword_query, args.num_results],
                 outputs=[gallery, code])
        b3.click(find_image_sql, inputs=[sql_query], outputs=[gallery, code])

    demo.launch()

# %%



