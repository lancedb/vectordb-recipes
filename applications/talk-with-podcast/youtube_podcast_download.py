#python3 -m pip install --force-reinstall https://github.com/yt-dlp/yt-dlp/archive/master.tar.gz

from __future__ import unicode_literals
import yt_dlp as youtube_dl
import streamlit as st

@st.cache_resource
def podcast_audio_retreival(video_link):
    # Download Audio of Youtube Podcast 
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_link])
        
        