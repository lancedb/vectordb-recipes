# Talk to Podcast

Using this application, You can talk to any Youtube Podcast. All you need is following requirements installed in your system.

1. Install Dependencies
```
pip install -r requirements.txt
pip install insanely-fast-whisper --force --ignore-requires-python
```
2. Ollama Installation
```
curl https://ollama.ai/install.sh | sh
ollama pull llama2
```

### Youtube Demo
[<img src="https://github.com/lancedb/vectordb-recipes/blob/main/assets/talk-with-podcast.png">](https://youtu.be/AGpl1h5K5v4)

You are ready to start

## Run Streamlit App

- Run Application
```
OPENAI_API_KEY=sk-... streamlit run app.py
```
