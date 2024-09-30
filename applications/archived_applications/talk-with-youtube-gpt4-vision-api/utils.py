import cv2
import base64
import openai
import streamlit as st


def base64_converter(video_path):
    video = cv2.VideoCapture(video_path)
    base64Frames = []
    while video.isOpened():
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

    video.release()

    return base64Frames


def prompting(base64Frames, openai_key):
    if len(base64Frames) < 5000:
        base64Frames = base64Frames[::50]
    elif len(base64Frames) < 10000:
        base64Frames = base64Frames[::100]
    elif len(base64Frames) < 100000:
        base64Frames = base64Frames[::10000]
    else:
        st.error("Video is too large to handle by GPT4 Vision API", icon="🚨")
    base64Frames = base64Frames[:50] if len(base64Frames) > 50 else base64Frames
    PROMPT_MESSAGES = [
        {
            "role": "user",
            "content": [
                "These are frames from a video that I want to upload. Generate a description so that I can get all the information about video to chat with it.",
                *map(lambda x: {"image": x, "resize": 756}, base64Frames),
            ],
        },
    ]

    params = {
        "model": "gpt-4-vision-preview",
        "messages": PROMPT_MESSAGES,
        "api_key": openai_key,
        "headers": {"Openai-Version": "2020-11-07"},
        "max_tokens": 300,
    }

    result = openai.ChatCompletion.create(**params)
    return result.choices[0].message.content
