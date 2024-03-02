import lancedb
import lancedb.embeddings.imagebind
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
import gradio as gr
from downloader import dowload_and_save_audio, dowload_and_save_image, base_path

model = get_registry().get("imagebind").create()


class TextModel(LanceModel):
    text: str
    image_uri: str = model.SourceField()
    audio_path: str
    vector: Vector(model.ndims()) = model.VectorField()


text_list = ["A bird", "A dragon", "A car","A guitar","A witch","Thunder"]
image_paths = dowload_and_save_image()
audio_paths = dowload_and_save_audio()

# Load data
inputs = [
    {"text": a, "audio_path": b, "image_uri": c}
    for a, b, c in zip(text_list, audio_paths, image_paths)
]

db = lancedb.connect("/tmp/lancedb")
table = db.create_table("img_bind", schema=TextModel)
table.add(inputs)


def process_image(inp_img) -> str:
    actual = (
        table.search(inp_img, vector_column_name="vector")
        .limit(1)
        .to_pydantic(TextModel)[0]
    )

    return actual.text, actual.audio_path


def process_text(inp_text) -> str:
    actual = (
        table.search(inp_text, vector_column_name="vector")
        .limit(1)
        .to_pydantic(TextModel)[0]
    )

    return actual.image_uri, actual.audio_path


def process_audio(inp_audio) -> str:
    actual = (
        table.search(inp_audio, vector_column_name="vector")
        .limit(1)
        .to_pydantic(TextModel)[0]
    )

    return actual.image_uri, actual.text


im_to_at = gr.Interface(
    process_image,
    gr.Image(type="filepath", value=image_paths[0]),
    [gr.Text(label="Output Text"), gr.Audio(label="Output Audio")],
    examples=image_paths,
    allow_flagging="never",
)
txt_to_ia = gr.Interface(
    process_text,
    gr.Textbox(label="Enter a prompt:"),
    [gr.Image(label="Output Image"), gr.Audio(label="Output Audio")],
    allow_flagging="never",
    examples=text_list,
)
a_to_it = gr.Interface(
    process_audio,
    gr.Audio(type="filepath", value=audio_paths[0]),
    [gr.Image(label="Output Image"), gr.Text(label="Output Text")],
    examples=audio_paths,
    allow_flagging="never",
)
demo = gr.TabbedInterface(
    [im_to_at, txt_to_ia, a_to_it],
    ["Image to Text/Audio", "Text to Image/Audio", "Audio to Image/Text"],
)

if __name__ == "__main__":
    demo.launch(share=True, allowed_paths=[f"{base_path}/test_inputs/"])
