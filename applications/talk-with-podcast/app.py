from youtube_podcast_download import podcast_audio_retreival
from transcribe_podcast import transcribe
from chat_retreival import retrieverSetup, chat

import os
import glob
import json
import streamlit as st
    
OPENAI_KEY =os.environ["OPENAI_API_KEY"]

@st.cache_resource
def video_data_retreival():
    f = open('output.json')
    data = json.load(f)
    
    #setting up reteriver
    qa = retrieverSetup(data["text"], OPENAI_KEY)
    return qa


st.header('Talk with Youtube Podcasts', divider='rainbow')

url = st.text_input('Youtube Link')

if url :
    st.video(url)
    # Podcast Audio Retreival from Youtube
    podcast_audio_retreival(url)

    # Trascribing podcast audio
    filename = glob.glob("*.mp3")[0]
    transcribe(filename)
    
    # Chat Agent getting ready
    qa = video_data_retreival()
    

prompt = st.chat_input("Talk with Podcast")
if prompt:
    st.write(f"{prompt}")
    #chat using retreiver
    answer = chat(qa, prompt)
    st.write(f"{answer}")