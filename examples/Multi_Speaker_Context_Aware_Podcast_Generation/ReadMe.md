# Multi Speaker Context Aware AI Podcast Generation
A comprehensive tool that transforms blog content into engaging podcast-style conversations with realistic text-to-speech synthesis.
![image](https://github.com/user-attachments/assets/24749a51-0113-46fd-8100-3a75c89e168f)

**Colab Link** : [Click Here](https://colab.research.google.com/github.com/shuklaji28/vectordb-recipes/blob/main/examples/Multi_Speaker_Context_Aware_Podcast_Generation/Multi_Speaker_Context_Aware_Podcast_Generation.ipynb
) 
## 🎙️ Features

- **Blog Content Scraping**: Extract content from Medium and other blogging platforms
- **Conversational Transformation**: Convert monologue blog posts into natural multi-speaker dialogues
- **Text-to-Speech Integration**: Generate realistic audio using multiple TTS services:
  - ElevenLabs API for premium voice quality
  - Smallest AI for efficient voice synthesis
- **Vector Database Storage**: Store and search podcast content using LanceDB
- **Multilingual Support**: Generate podcasts in multiple languages (can be implemented with Bhashini Integration or Gemini itself)

## **High Level Architecture**

![image](https://github.com/user-attachments/assets/8fd06462-a1b9-4641-8c09-711f5e43a490)


## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Required Python packages (install via `pip install -r requirements.txt`)
- API keys for ElevenLabs and Smallest AI
- LanceDB installed locally
  
### 🔍 How It Works

**Content Extraction**: The system scrapes blog content using BeautifulSoup, handling various blog platforms and structures.
**Conversation Generation**: The monologue blog content is transformed into a natural-sounding conversation between multiple speakers.
**Audio Synthesis**: For each speaker's part, the appropriate TTS service is used to generate audio with distinct voices.
**Vector Storage**: Conversations are stored in LanceDB with embeddings for efficient semantic search.

### 🔮 Future Enhancements

1. Interactive podcast experience with user input
2. Background music and sound effects
3. Enhanced multilingual support with Bhashini
4. Voice emotion and tone adjustment based on content sentiment
5. Web interface for easy content uploading and podcast generation
