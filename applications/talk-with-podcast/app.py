from youtube_podcast_download import podcast_audio_retreival
from transcribe_podcast import transcribe
from chat_retreival import retrieverSetup, chat
from langroid_utils import configure, agent

import os
import glob
import json
import streamlit as st
    
OPENAI_KEY =os.environ["OPENAI_API_KEY"]

@st.cache_resource
def video_data_retreival(framework):
    f = open('output.json')
    data = json.load(f)
    
    #setting up reteriver
    if framework == "Langchain":
        qa = retrieverSetup(data["text"], OPENAI_KEY)
        return qa
    elif framework == "Langroid":
        langroid_file = open("langroid_doc.txt","w") # write mode
        langroid_file.write(data["text"])
        cfg = configure("langroid_doc.txt")
        return cfg


    


st.header('Talk with Youtube Podcasts', divider='rainbow')

url = st.text_input('Youtube Link')
framework = st.radio(
        "**Select Framework 👇**",
        ["Langchain", "Langroid"],
        key="Langchain",)

if url :
    st.video(url)
    # Podcast Audio Retreival from Youtube
    podcast_audio_retreival(url)

    # Trascribing podcast audio
    filename = glob.glob("*.mp3")[0]
    transcribe(filename)
    
    st.markdown(f"##### `{framework}` Framework Selected for Talk with Podcast")
    # Chat Agent getting ready
    qa = video_data_retreival(framework)
        

    

prompt = st.chat_input("Talk with Podcast")

if prompt:
    st.write(f"{prompt}")
    #chat using retreiver
    if framework == "Langchain":
        answer = chat(qa, prompt)
    elif framework == "Langroid":
        answer = agent(qa, prompt)
    
    st.write(f"{answer}")