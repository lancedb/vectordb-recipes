from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionXLPipeline,
    AutoPipelineForText2Image,
)
import mlx.core as mx
from diffusion_mlx import StableDiffusion, StableDiffusionXL
import torch
from tqdm import tqdm
from PIL import Image
import numpy as np
import time

SUPPORTS_NEGATIVE_PROMPT = False
GLOBAL_NEGATIVE_PROMPT = (
    "3d, cartoon, anime, (deformed eyes, nose, ears, nose), bad anatomy, ugly, text"
)
RESPONSE_TO_DIFFUSER_PROMPT = "Get minimal text (no longer than 70 tokesn) describe the response and use it as a prompt for a diffuser: {} | avoid adding text to the image |"

"""
MODEL_MAP = {
    "runway_diffusion_v1": "runwayml/stable-diffusion-v1-5",
    "sdxl": "stabilityai/stable-diffusion-xl-base-1.0",
}

def load_model(model_id="runway_diffusion_v1"):
    global MODEL_PIPE, SUPPORTS_NEGATIVE_PROMPT
    if model_id == "runway_diffusion_v1":
        MODEL_PIPE = StableDiffusionPipeline.from_pretrained(MODEL_MAP[model_id])
    elif model_id == "sdxl":
        MODEL_PIPE = StableDiffusionXLPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-base-1.0", variant="fp16", use_safetensors=True
                )
        SUPPORTS_NEGATIVE_PROMPT = True
    elif model_id == "sdxl-turbo":
        MODEL_PIPE = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", variant="fp16")



def generate_image(prompt, model_id="runway_diffusion_v1"):
    prompt += " | avoid adding text to the image |"
    image = MODEL_PIPE(prompt).images[0] if not SUPPORTS_NEGATIVE_PROMPT else MODEL_PIPE(prompt, negative_prompt=GLOBAL_NEGATIVE_PROMPT).images[0]
    return image
"""

### MLX version
import mlx.core as mx
import mlx.nn as nn


def load_models(model="sdxl", float16=True, quantize=True, preload_models=True):
    # Load the models
    if model == "sdxl":
        model = StableDiffusionXL("stabilityai/sdxl-turbo", float16=float16)
        if quantize:
            nn.quantize(
                model.text_encoder_1,
                class_predicate=lambda _, m: isinstance(m, nn.Linear),
            )
            nn.quantize(
                model.text_encoder_2,
                class_predicate=lambda _, m: isinstance(m, nn.Linear),
            )
            nn.quantize(model.unet, group_size=32, bits=8)
        steps = 2
    else:
        model = StableDiffusion(
            "stabilityai/stable-diffusion-2-1-base", float16=float16
        )
        if quantize:
            nn.quantize(
                model.text_encoder,
                class_predicate=lambda _, m: isinstance(m, nn.Linear),
            )
            nn.quantize(model.unet, group_size=32, bits=8)
        steps = 50

    # Ensure that models are read in memory if needed
    if preload_models:
        model.ensure_models_are_loaded()

    return model, steps


def generate_image(model, steps, prompt, verbose=True):
    # Generate the latent vectors using diffusion
    time1 = time.time()
    latents = model.generate_latents(
        prompt,
        n_images=1,
        num_steps=steps,
        negative_text=GLOBAL_NEGATIVE_PROMPT,
    )
    for x_t in tqdm(latents, total=steps):
        mx.eval(x_t)

    # The following is not necessary but it may help in memory
    # constrained systems by reusing the memory kept by the unet and the text
    # encoders.

    # if model == "sdxl":
    #     del MODEL_PIPE.text_encoder_1
    #     del MODEL_PIPE.text_encoder_2
    # else:
    #     del MODEL_PIPE.text_encoder
    # del sd.unet
    # del sd.sampler
    peak_mem_unet = mx.metal.get_peak_memory() / 1024**3

    # Decode them into images
    decoded = []
    for i in tqdm(range(0, 1, 1)):
        decoded.append(model.decode(x_t[i : i + 1]))
        mx.eval(decoded[-1])
    peak_mem_overall = mx.metal.get_peak_memory() / 1024**3

    # Arrange them on a grid
    x = mx.concatenate(decoded, axis=0)
    x = mx.pad(x, [(0, 0), (8, 8), (8, 8), (0, 0)])
    B, H, W, C = x.shape
    x = x.reshape(1, B, H, W, C).transpose(0, 2, 1, 3, 4)
    x = x.reshape(1 * H, B * W, C)
    x = (x * 255).astype(mx.uint8)

    time2 = time.time()
    if verbose:
        print(f"Time taken to generate the image: {time2 - time1:.3f}s")
    # Save them to disc
    im = Image.fromarray(np.array(x))

    # Report the peak memory used during generation
    if verbose:
        print(f"Peak memory used for the unet: {peak_mem_unet:.3f}GB")
        print(f"Peak memory used overall:      {peak_mem_overall:.3f}GB")

    return im


if __name__ == "__main__":
    load_models()
    generate_image("A cartoon of a cute cat", verbose=True)
    generate_image("Hogwartz school of witchcraft and wizardry", verbose=True)
