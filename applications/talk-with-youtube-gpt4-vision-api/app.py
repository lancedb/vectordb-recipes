import streamlit as st
from download_video import download
from utils import base64_converter, prompting
from chat_retreival import retrieverSetup, chat
import os

OPENAI_KEY = os.environ["OPENAI_API_KEY"]


@st.cache_data
def video_data_retreival(url):
    # download video
    video_path = download(url)
    # convert video frames into base64
    base64Frames = base64_converter(video_path)
    # using GPT4 vision for description generation
    prompt_output = prompting(base64Frames, OPENAI_KEY)
    # setting up reteriver
    qa = retrieverSetup(prompt_output, OPENAI_KEY)
    return qa


st.header("Talk with Youtube Videos", divider="rainbow")

url = st.text_input("Youtube Link")

if url:
    st.video(url)
    qa = video_data_retreival(url)


prompt = st.chat_input("Talk with Video")
if prompt:
    st.write(f"{prompt}")
    # chat using retreiver
    answer = chat(qa, prompt)
    st.write(f"{answer}")
