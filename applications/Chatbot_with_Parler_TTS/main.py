import gradio as gr
from rag_lance import get_rag_output
from tts_module import text_to_speech


def process_question(question, include_audio):
    generated_text = get_rag_output(question)
    if include_audio:
        audio_file_path = text_to_speech(generated_text)
        return generated_text, audio_file_path
    else:
        return generated_text, None  # Return None for the audio part


iface = gr.Interface(
    fn=process_question,
    inputs=[
        gr.Textbox(lines=2, placeholder="Enter a question..."),
        gr.Checkbox(
            label="Include audio", value=True
        ),  # Default to True, can be unchecked by user
    ],
    outputs=[
        gr.Textbox(label="Generated Text"),
        gr.Audio(label="Generated Audio", type="filepath"),  # No optional keyword
    ],
    title="Advance RAG chatbot with TTS support",
    description="Ask a question and get a text response along with its audio representation. Optionally, include the audio response.",
    examples=[
        ["What is net profit of Airbnb ?"],
        [
            "What are the specific factors contributing to Airbnb's increased operational expenses in the last fiscal year"
        ],
    ],
)

if __name__ == "__main__":
    iface.launch(debug=True, share=True)
