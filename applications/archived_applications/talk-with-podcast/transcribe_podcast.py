import os
import streamlit as st


@st.cache_resource
def transcribe(filename):
    os.system(
        "insanely-fast-whisper  --model-name distil-whisper/large-v2 --file-name {filename}"
    )
    os.remove(filename)
