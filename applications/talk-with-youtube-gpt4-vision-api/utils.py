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
    if len(base64Frames)< 10:
        base64Frames = base64Frames
    elif len(base64Frames) < 100:
        base64Frames = base64Frames[0::10]
    elif len(base64Frames) < 1000:
        base64Frames = base64Frames[0::100]
    elif len(base64Frames) < 10000:
        base64Frames = base64Frames[0::1000]
    else:
        st.error('Video is too large to handle by GPT4 Vision API', icon="🚨")

    PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames from a video that I want to upload. Generate a description so that I can get all the information about video to chat with it.",
            *map(lambda x: {"image": x, "resize": 360}, base64Frames),],},]
    
    params = {
        "model": "gpt-4-vision-preview",
        "messages": PROMPT_MESSAGES,
        "api_key": openai_key,
        "headers": {"Openai-Version": "2020-11-07"},
        "max_tokens": 200,
    }

    result = openai.ChatCompletion.create(**params)
    return result.choices[0].message.content