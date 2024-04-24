import torch
import soundfile as sf
from transformers import AutoTokenizer
from parler_tts import ParlerTTSForConditionalGeneration


def text_to_speech(text, filename="output_audio.wav"):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model = ParlerTTSForConditionalGeneration.from_pretrained(
        "parler-tts/parler_tts_mini_v0.1"
    ).to(device)
    tokenizer = AutoTokenizer.from_pretrained("parler-tts/parler_tts_mini_v0.1")

    # description = "A clear and articulate Indian English male voice with a medium pitch and neutral accent  with a friendly and engaging tone. The audio quality is high, ensuring that each word is easily understandable without any background noise."
    description = "Utilize a male voice with a low pitch and an Indian English accent for the chatbot. The speech should be fast yet clear, ensuring each word is distinctly articulated in a crisp and confined audio environment."
    input_ids = tokenizer(description, return_tensors="pt").input_ids.to(device)
    prompt_input_ids = tokenizer(text, return_tensors="pt").input_ids.to(device)

    generation = model.generate(input_ids=input_ids, prompt_input_ids=prompt_input_ids)
    audio_arr = generation.cpu().numpy().squeeze()
    sf.write(filename, audio_arr, model.config.sampling_rate)

    return filename
