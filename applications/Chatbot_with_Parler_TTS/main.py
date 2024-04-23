import gradio as gr
from rag_lance import get_rag_output
from tts_module import text_to_speech

def process_question(question):
    generated_text = get_rag_output(question)
    audio_file_path = text_to_speech(generated_text)
    return generated_text, audio_file_path

iface = gr.Interface(
    fn=process_question,
    inputs=gr.Textbox(lines=2, placeholder="Enter a question..."),
    outputs=[
        gr.Textbox(label="Generated Text"),
        gr.Audio(label="Generated Audio", type="filepath")
    ],
    title="Question Answering with TTS support",
    description="Ask a question and get a text response along with its audio representation."
)

if __name__ == "__main__":
    iface.launch(debug=True, share=True)
