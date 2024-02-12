from langroid.utils.configuration import settings
from utils import configure, agent

import streamlit as st
import os

settings.cache_type = "fakeredis"

st.header("DocChatAgent by Langroid", divider="rainbow")

uploadedFile = st.file_uploader("Choose a txt file")

if uploadedFile is not None:
    with open(os.path.join("tempDir", uploadedFile.name), "wb") as f:
        f.write(uploadedFile.getbuffer())

    # configure
    cfg = configure(uploadedFile.name)

prompt = st.chat_input("Talk with Document")
if prompt:
    st.write(f"{prompt}")

    # chat using docchatagent
    answer = agent(cfg, prompt)
    st.write(f"{answer}")
