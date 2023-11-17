# VectorDB-recipes
<br />
Dive into building GenAI applications!
This repository contains examples, applications, starter code, & tutorials to help you kickstart your GenAI projects.

- These are built using LanceDB, a free, open-source, serverless vectorDB that **requires no setup**. 
- It **integrates into python data ecosystem** so you can simply start using these in your existing data pipelines in pandas, arrow, pydantic etc.
- LanceDB has **native Typescript SDK** using which you can **run vector search** in serverless functions!

<img src="./assets/lancedb-illustration.png" height="85%" width="85%" />
<br />
Join our community for support - <a href="https://discord.gg/zMM32dvNtd">Discord</a> •
<a href="https://twitter.com/lancedb">Twitter</a>

---

This repository is divided into 3 sections:
- [Examples](#examples) - Get right into the code with minimal introduction, aimed at getting you from an idea to PoC within minutes!
- [Applications](#projects--applications) - Ready to use Python and web apps using applied LLMs, VectorDB and GenAI tools
- [Tutorials](#tutorials) - A curated list of tutorials, blogs, Colabs and courses to get you started with GenAI in greater depth. 

## Examples
Applied examples that get right into the code with minimal introduction, aimed at getting you from an idea to PoC within minutes!
Examples are available as:
* **Colab notebooks** - that builds the application is stages allowing you to investigate results at every intermediate stage.
* **Python scripts** - for cases where you'd like directly to use the file or snippets to integrate in your application
* **JS/TS scripts** - Some examples are written using lancedb's native js library! These script/snippets can also be directly integrated in your web applications.

If you're looking for in-depth tutorial-like examples, checkout the [tutorials](#tutorials) section!

| Example | Interactive Envs | Scripts  |
|-------- | ---------------- | ------   |
| | | |
| [Youtube transcript search bot](./examples/youtube_bot/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/youtube_bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/youtube_bot/main.py)  [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/youtube_bot/index.js)|
| [Langchain: Code Docs QA bot](./examples/Code-Documentation-QA-Bot/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Code-Documentation-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/Code-Documentation-QA-Bot/main.py)  [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/Code-Documentation-QA-Bot/index.js)|
| [AI Agents: Reducing Hallucination](./examples/reducing_hallucinations_ai_agents/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/reducing_hallucinations_ai_agents/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/reducing_hallucinations_ai_agents/main.py)  [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/reducing_hallucinations_ai_agents/index.js)|
| [Multimodal CLIP: DiffusionDB](./examples/multimodal_clip/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_clip/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/multimodal_clip/main.py)  |
| [Multimodal CLIP: Youtube videos](./examples/multimodal_video_search/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_video_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/multimodal_video_search/main.py)  |
| [TransformersJS Embedding example](./examples/js-transformers/) | | [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/js-transformers/index.js)  |
| [Movie Recommender](./examples/movie-recommender/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/movie-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/movie-recommender/main.py)  |
| [Product Recommender](./examples/product-recommender/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/product-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/product-recommender/main.py)  |
| [Audio Search](./examples/audio_search/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/audio_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/audio_search/main.py)  |
| [Multimodal Image + Text Search](./examples/multimodal_search/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/multimodal_search/main.py)  |
| [Evaluating Prompts with Prompttools](./examples/prompttools-eval-prompts/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/prompttools-eval-prompts/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> |  |
| [Arxiv paper recommender](./examples/arxiv-recommender) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/arxiv-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/arxiv-recommender/main.py)   |
| [Multi-lingual search](./examples/multi-lingual-wiki-qa) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multi-lingual-wiki-qa/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](.examples/multi-lingual-wiki-qa/main.py)   |
| [Instruct-Multitask](./examples/instruct-multitask) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/instruct-multitask/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](.examples/instruct-multitask/main.py)   |
| [Facial Recognition](./examples/facial_recognition) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/facial_recognition/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](.examples/facial_recognition/main.py)   |





## Projects & Applications
These are ready to use applications built using LanceDB serverless vector database. You can explore these open source projects, use parts of them in your projects or build your applications on top of these. 

| Project Name                                        | Description                                                                                                          | Screenshot                                |
|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| [YOLOExplorer](https://github.com/lancedb/yoloexplorer) | Iterate on your YOLO / CV datasets using SQL, Vector semantic search, and more within seconds                  | ![YOLOExplorer](https://github.com/lancedb/vectordb-recipes/assets/15766192/ae513a29-8f15-4e0b-99a1-ccd8272b6131) |
| [Website Chatbot (Deployable Vercel Template)](https://github.com/lancedb/lancedb-vercel-chatbot) | Create a chatbot from the sitemap of any website/docs of your choice. Built using vectorDB serverless native javascript package. | ![Chatbot](assets/vercel-template.gif)    |
| [Multi-Modal Search Engine](https://github.com/lancedb/vectordb-recipes/tree/rf/applications/multimodal-search) | Create a Multi-modal search engine app, to search images using both images or text | ![Search](https://github.com/lancedb/vectordb-recipes/assets/15766192/9805fec8-da72-44c0-be12-ddbe1c2d6afc)|
| [ Chat with multiple  URL/website  ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/chat_with_anywebsite/) | Conversational AI for Any Website with Mistral,Bge Embedding & LanceDB |![webui_aa](https://github.com/akashAD98/vectordb-recipes/assets/62583018/47a9af87-2d94-4fd8-afa1-373db03bd728)  |
| [ Hr chatbot  ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/HR_chatbot/) | Hr chatbot - ask your personal query using zero-shot React agent & tools |![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/0ea78428-44be-4bff-874b-79b1fcc3b7d6)|
| [ Talk with Youtube Video using GPT4 Vision API ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/talk-with-youtube-gpt4-vision-api/) | Talk with Youtube Video using GPT4 Vision API and Langchain |![demo](https://github.com/PrashantDixit-dev/vectordb-recipes/assets/54981696/e46f191d-d9e3-41a8-9598-a1a79b4b89c4)



## Tutorials
Looking to get starte with LLMs, vectorDBs, and the world of Generative AI? These in-depth tutorials and courses cover these concepts with practical follow along colabs where possible.
| Tutorial | Interactive Environment | Blog Link |
| --------- | -------------------------- | ----------- |
|           |                            |             |
| [LLMs, RAG, & the missing storage layer for AI](https://medium.com/etoai/llms-rag-the-missing-storage-layer-for-ai-28ded35fa984) | | [Read the Blog](https://medium.com/etoai/llms-rag-the-missing-storage-layer-for-ai-28ded35fa984) |
| [Fine-Tuning LLM using PEFT & QLoRA](./tutorials/fine-tuning_LLM_with_PEFT_QLoRA) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/chatbot_using_Llama2_&_lanceDB/main.ipynb) | [Read the Blog](https://blog.lancedb.com/optimizing-llms-a-step-by-step-guide-to-fine-tuning-with-peft-and-qlora-22eddd13d25b) |
| [Context-Aware Chatbot using Llama 2 & LanceDB](./tutorials/chatbot_using_Llama2_&_lanceDB) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/fine-tuning_LLM_with_PEFT_QLoRA/main.ipynb) | [Read the Blog](https://blog.lancedb.com/context-aware-chatbot-using-llama-2-lancedb-as-vector-database-4d771d95c755) |
| [A Primer on Text Chunking and its Types](./tutorials/different-types-text-chunking-in-RAG) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/different-types-text-chunking-in-RAG/Text_Chunking_on_RAG_application_with_LanceDB.ipynb) | [Read the Blog](https://blog.lancedb.com/a-primer-on-text-chunking-and-its-types-a420efc96a13) |
| [NER-powered Semantic Search using LanceDB](./tutorials/NER-powered-Semantic-Search-with-LanceDB) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/NER-powered-Semantic-Search-with-LanceDB/NER_powered_Semantic_Search_with_LanceDB.ipynb) | [Read the Blog](https://prasantdixit.medium.com/ner-powered-semantic-search-using-lancedb-51051dc3e493) |



**🌟 New! 🌟 Applied GenAI and VectorDB course on Udacity**
Learn about GenAI and vectorDBs using LanceDB in the recently launched [Udacity Course](https://www.udacity.com/course/building-generative-ai-solutions-with-vector-databases--cd12952)


<img src="./assets/udacity-course.png" width="80%" height="80%" />


## Contributing Examples
If you're working on some cool applications that you'd like to add to this repo, please open a PR!
