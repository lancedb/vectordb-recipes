import lancedb
import lancedb.embeddings.imagebind
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
import gradio as gr
from downloader import dowload_and_save_audio, dowload_and_save_image

model = get_registry().get("imagebind").create()


class TextModel(LanceModel):
    text: str
    image_uri: str = model.SourceField()
    audio_path: str
    vector: Vector(model.ndims()) = model.VectorField()


text_list = ["A bird", "A dragon", "A car"]
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


css = """
output-audio, output-text {
display: None
}
img { 
# width: 500px; 
# height: 450px; 
margin-left: auto;
margin-right: auto;
object-fit: cover;

"""
with gr.Blocks(css=css) as app:
    # Using Markdown for custom CSS (optional)
    with gr.Tab("Image to Text and Audio"):
        with gr.Row():
            with gr.Column():
                inp1 = gr.Image(
                    value=image_paths[0],
                    type="filepath",
                    elem_id="img",
                    interactive=False,
                )
                output_audio1 = gr.Audio(label="Output Audio", elem_id="output-audio")
                output_text1 = gr.Textbox(label="Output Text", elem_id="output-text")
                btn_img1 = gr.Button("Retrieve")

                # output_audio1 = gr.Audio(label="Output Audio 1", elem_id="output-audio1")
            with gr.Column():
                inp2 = gr.Image(
                    value=image_paths[1],
                    type="filepath",
                    elem_id="img",
                    interactive=False,
                )
                output_audio2 = gr.Audio(label="Output Audio", elem_id="output-audio")
                output_text2 = gr.Textbox(label="Output Text", elem_id="output-text")
                btn_img2 = gr.Button("Retrieve")

            with gr.Column():
                inp3 = gr.Image(
                    value=image_paths[2],
                    type="filepath",
                    elem_id="img",
                    interactive=False,
                )
                output_audio3 = gr.Audio(label="Output Audio", elem_id="output-audio")
                output_text3 = gr.Textbox(label="Output Text", elem_id="output-text")
                btn_img3 = gr.Button("Retrieve")

    with gr.Tab("Text to Image and Audio"):
        with gr.Row():
            with gr.Column():
                input_txt1 = gr.Textbox(label="Enter a prompt:", elem_id="output-text")
                output_audio4 = gr.Audio(label="Output Audio", elem_id="output-audio")
                output_img1 = gr.Image(type="filepath", elem_id="img")

    with gr.Tab("Audio to Image and Text"):
        with gr.Row():
            with gr.Column():
                inp_audio1 = gr.Audio(
                    value=audio_paths[0], type="filepath", interactive=False
                )
                output_img7 = gr.Image(type="filepath", elem_id="img")
                output_text7 = gr.Textbox(label="Output Text", elem_id="output-text")
                btn_audio1 = gr.Button("Retrieve")

            with gr.Column():
                inp_audio2 = gr.Audio(
                    value=audio_paths[1], type="filepath", interactive=False
                )
                output_img8 = gr.Image(type="filepath", elem_id="img")
                output_text8 = gr.Textbox(label="Output Text", elem_id="output-text")
                btn_audio2 = gr.Button("Retrieve")

            with gr.Column():
                inp_audio3 = gr.Audio(
                    value=audio_paths[2], type="filepath", interactive=False
                )
                output_img9 = gr.Image(type="filepath", elem_id="img")
                output_text9 = gr.Textbox(label="Output Text", elem_id="output-text")
                btn_audio3 = gr.Button("Retrieve")

    # Click actions for buttons/Textboxes
    btn_img1.click(process_image, inputs=[inp1], outputs=[output_text1, output_audio1])
    btn_img2.click(process_image, inputs=[inp2], outputs=[output_text2, output_audio2])
    btn_img3.click(process_image, inputs=[inp3], outputs=[output_text3, output_audio3])

    input_txt1.submit(
        process_text, inputs=[input_txt1], outputs=[output_img1, output_audio4]
    )

    btn_audio1.click(
        process_audio, inputs=[inp_audio1], outputs=[output_img7, output_text7]
    )
    btn_audio2.click(
        process_audio, inputs=[inp_audio2], outputs=[output_img8, output_text8]
    )
    btn_audio3.click(
        process_audio, inputs=[inp_audio3], outputs=[output_img9, output_text9]
    )

if __name__ == "__main__":
    app.launch(share=True, allowed_paths=["./test_inputs/"])
