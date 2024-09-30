from chat_retreival import retrieverSetup, chat

import os
import streamlit as st

OPENAI_KEY = os.environ["OPENAI_API_KEY"]


@st.cache_resource
def loading_wiki_pages(query):
    # Setting Up Reteriver
    qa = retrieverSetup(query, OPENAI_KEY)
    return qa


st.header("Talk with Wikipedia Pages", divider="violet")

query_wiki = st.text_input("Enter Topic")
if query_wiki:
    # Chat Agent getting ready
    qa = loading_wiki_pages(query_wiki)

prompt = st.chat_input("Enter Prompt")

if prompt:
    user = st.chat_message("user")
    user.write(f"{prompt}")

    # chat using retreiver
    answer = chat(qa, prompt)
    assistant = st.chat_message("ai")
    assistant.write(f"{answer}")
