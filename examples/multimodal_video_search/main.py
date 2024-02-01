import argparse
import duckdb
import lancedb
import pyarrow.compute as pc
from transformers import CLIPModel, CLIPProcessor, CLIPTokenizerFast
import gradio as gr

MODEL_ID = None
MODEL = None
TOKENIZER = None
PROCESSOR = None


def get_table():
    db = lancedb.connect("data/video-lancedb")
    return db.open_table("multimodal_video")


def setup_clip_model(model_id):
    global MODEL_ID, MODEL, TOKENIZER, PROCESSOR
    MODEL_ID = model_id
    TOKENIZER = CLIPTokenizerFast.from_pretrained(MODEL_ID)
    MODEL = CLIPModel.from_pretrained(MODEL_ID)
    PROCESSOR = CLIPProcessor.from_pretrained(MODEL_ID)


def embed_func(query):
    inputs = TOKENIZER([query], padding=True, return_tensors="pt")
    text_features = MODEL.get_text_features(**inputs)
    return text_features.detach().numpy()[0]


def find_video_vectors(query):
    emb = embed_func(query)
    code = (
        "import lancedb\n"
        "db = lancedb.connect('data/video-lancedb')\n"
        "tbl = db.open_table('multimodal_video')\n\n"
        f"embedding = embed_func('{query}')\n"
        "tbl.search(embedding).limit(9).to_df()"
    )
    return (_extract(tbl.search(emb).limit(9).to_df()), code)


def find_video_keywords(query):
    code = (
        "import lancedb\n"
        "db = lancedb.connect('data/video-lancedb')\n"
        "tbl = db.open_table('multimodal_video')\n\n"
        f"tbl.search('{query}').limit(9).to_df()"
    )
    return (_extract(tbl.search(query).limit(9).to_df()), code)


def find_video_sql(query):
    code = (
        "import lancedb\n"
        "import duckdb\n"
        "db = lancedb.connect('data/video-lancedb')\n"
        "tbl = db.open_table('multimodal_video')\n\n"
        "videos = tbl.to_lance()\n"
        f"duckdb.sql('{query}').to_df()"
    )
    videos = tbl.to_lance()
    return (_extract(duckdb.sql(query).to_df()), code)


def _extract(df):  # Define a 3x3 Python list to store the HTML code
    video_id_col = "video_id"
    start_time_col = "start_time"
    grid_html = '<div style="display: grid; grid-template-columns: repeat(3, 1fr); grid-gap: 20px;">'

    for _, row in df.iterrows():
        iframe_code = f'<iframe width="100%" height="315" src="https://www.youtube.com/embed/{row[video_id_col]}?start={str(row[start_time_col])}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
        grid_html += f'<div style="width: 100%;">{iframe_code}</div>'

    grid_html += "</div>"
    return grid_html


def create_gradio_dash():
    with gr.Blocks() as demo:
        gr.Markdown(
            """
                    # Multimodal Video Search with LanceDB
                    We used LanceDB to store frames every thirty seconds and the title of 13000+ videos, 5 random from each top category from the Youtube 8M dataset. 
                    Then, we used the CLIP model to embed frames and titles together. With LanceDB, we can perform embedding, keyword, and SQL search on these videos.
                    """
        )
        with gr.Row():
            with gr.Tab("Embeddings"):
                vector_query = gr.Textbox(value="retro gaming", show_label=False)
                b1 = gr.Button("Submit")
            with gr.Tab("Keywords"):
                keyword_query = gr.Textbox(value="ninja turtles", show_label=False)
                b2 = gr.Button("Submit")
            with gr.Tab("SQL"):
                sql_query = gr.Textbox(
                    value="SELECT DISTINCT video_id, * from videos WHERE start_time > 0 LIMIT 9",
                    show_label=False,
                )
                b3 = gr.Button("Submit")
        with gr.Row():
            code = gr.Code(label="Code", language="python")
        with gr.Row():
            gallery = gr.HTML()

        b1.click(find_video_vectors, inputs=vector_query, outputs=[gallery, code])
        b2.click(find_video_keywords, inputs=keyword_query, outputs=[gallery, code])
        b3.click(find_video_sql, inputs=sql_query, outputs=[gallery, code])

    demo.launch()


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_id", type=str, default="openai/clip-vit-base-patch32")
    return parser.parse_args()


if __name__ == "__main__":
    args = args_parse()
    setup_clip_model(args.model_id)
    tbl = get_table()
    create_gradio_dash()
