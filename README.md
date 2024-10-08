# VectorDB-recipes
<br />
Dive into building GenAI applications!
This repository contains examples, applications, starter code, & tutorials to help you kickstart your GenAI projects.

- These are built using LanceDB, a free, open-source, serverless vectorDB that **requires no setup**. 
- It **integrates into Python data ecosystem** so you can simply start using these in your existing data pipelines in pandas, arrow, pydantic etc.
- LanceDB has **native Typescript SDK** using which you can **run vector search** in serverless functions!

<img src="https://github.com/lancedb/vectordb-recipes/assets/5846846/d284accb-24b9-4404-8605-56483160e579" height="85%" width="85%" />

<br />
Join our community for support - <a href="https://discord.gg/zMM32dvNtd">Discord</a> •
<a href="https://twitter.com/lancedb">Twitter</a>

---

This repository is divided into 2 sections:
- [Examples](#examples) - Get right into the code with minimal introduction, aimed at getting you from an idea to PoC within minutes!
- [Applications](#projects--applications) - Ready to use Python and web apps using applied LLMs, VectorDB and GenAI tools


The following examples are organized into different tables to make similar types of examples easily accessible.

### Sections

- [Build from Scratch](#build-from-scratch) - Build applications/examples from scratch using LanceDB for efficient vector-based document retrieval.
- [Multimodal](#multimodal) - Build a multimodal search application with input text or image as queries.
- [RAG](#rag) - Build a variety of RAG by loading data from different formats and query with text.
- [Vector Search](#vector-search) - Build vector search application using different search algorithms.
- [Chatbot](#chatbot) - Build chatbot application where user input queries to retrieve relevant context and generate coherent, context-aware replies.
- [Evalution](#evaluation) - Evaluate reference and candidate texts to measure their performance on various metrics.
- [AI Agents](#ai-agents) - Design an application powered with AI agents to exchange information, coordinate tasks, and achieve shared goals effectively.
- [Recommender Systems](#recommender-systems) - Build Recommendation systems which generate personalized recommendations and enhance user experience.
- [Concepts](#concepts) - Concepts related to LLM applications pipeline to ensures accurate information retrieval.


### 🌟 New 🌟 
- Vision Retrieval with ColPali -  <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/ColPali-vision-retriever/colpali.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
- Social media posts caption generation with Llama3.2-11B-Vision - <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/social-media-caption-generation-with-llama3.2/social_media_caption_generation_llama3_2_11B.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>




### Build from Scratch

Build applications/examples using LanceDB for efficient vector-based document retrieval.

| Build from Scratch &nbsp; &nbsp;| Interactive Notebook & Scripts &nbsp; | 
|-------- | -------------: |
|||
| [Build RAG from Scratch](./tutorials/RAG-from-Scratch) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/RAG-from-Scratch/RAG_from_Scratch.ipynb) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|  |
| [Local RAG from Scratch with Llama3](./tutorials/Local-RAG-from-Scratch) | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./tutorials/Local-RAG-from-Scratch/rag.py) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|  |
| [Multi-Head RAG from Scratch](./tutorials/Multi-Head-RAG-from-Scratch/) | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./tutorials/Multi-Head-RAG-from-Scratch/main.py) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|  |
||||

### MultiModal

Create a multimodal search application using LanceDB for efficient vector-based retrieval of text and image data. Input text or image queries to find the most relevant documents and images from your corpus.

| Multimodal &nbsp; &nbsp;| Interactive Notebook & Scripts &nbsp; | Blog |
| --------- | -------------------------- | ----------- |
||||
| [Multimodal CLIP: DiffusionDB](/examples/multimodal_clip_diffusiondb/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_clip_diffusiondb/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/multimodal_clip_diffusiondb/main.py) [![LLM](https://img.shields.io/badge/local-llm-green)](#)    [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/multi-modal-ai-made-easy-with-lancedb-clip-5aaf8801c939/)|
| [Multimodal CLIP: Youtube videos](/examples/multimodal_video_search/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_video_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/multimodal_video_search/main.py) [![LLM](https://img.shields.io/badge/local-llm-green)](#)    [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/multi-modal-ai-made-easy-with-lancedb-clip-5aaf8801c939/)|
| [Cambrian-1: Vision centric exploration of images](https://www.kaggle.com/code/prasantdixit/cambrian-1-vision-centric-exploration-of-images/) | [![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/prasantdixit/cambrian-1-vision-centric-exploration-of-images/) [![LLM](https://img.shields.io/badge/local-llm-green)](#)   [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/cambrian-1-vision-centric-exploration/)|
| [Social Media Caption Generation using Llama3.2-11B-Vision](./examples/social-media-caption-generation-with-llama3.2/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/social-media-caption-generation-with-llama3.2/social_media_caption_generation_llama3_2_11B.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/local-llm-green)](#)    [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|
| [Efficient Vision retreiver with ColPali & LanceDB](/examples/ColPali-vision-retriever) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/ColPali-vision-retriever/colpali.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/local-llm-green)](#)    [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)| 
||||

### RAG

Develop a Retrieval-Augmented Generation (RAG) application using LanceDB for efficient vector-based information retrieval. Input text queries to retrieve relevant documents and generate comprehensive answers by combining retrieved information.

| RAG &nbsp; &nbsp;| Interactive Notebook & Scripts | Blog |
| --------- | -------------------------- | ----------- |
||||
| [RAG with Contextual Retrieval and Hybrid search](./examples/Contextual-RAG/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Contextual-RAG/Anthropic_Contextual_RAG.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#)  [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)||
| [RAG with Matryoshka Embeddings and LlamaIndex](./tutorials/RAG-with_MatryoshkaEmbed-Llamaindex/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/RAG-with_MatryoshkaEmbed-Llamaindex/RAG_with_MatryoshkaEmbedding_and_Llamaindex.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)||
| [RAG with IBM Watsonx](./examples/RAG-with-watsonx/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/RAG-with-watsonx/Watsonx_example.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![watsonx LLM](https://img.shields.io/badge/watsonx-api-lightblue)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)||
| [Improve RAG with Re-ranking](/examples/RAG_Reranking/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/RAG_Reranking/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/local-llm-green)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/simplest-method-to-improve-rag-pipeline-re-ranking-cf6eaec6d544)|
| [Instruct-Multitask](./examples/instruct-multitask) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/instruct-multitask/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/instruct-multitask/main.py)  [![LLM](https://img.shields.io/badge/local-llm-green)](#)   [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/multitask-embedding-with-lancedb-be18ec397543)|
| [Improve RAG with HyDE](/examples/Advance-RAG-with-HyDE/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Advance-RAG-with-HyDE/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>   [![LLM](https://img.shields.io/badge/openai-api-white)](#)  [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/advanced-rag-precise-zero-shot-dense-retrieval-with-hyde-0946c54dfdcb)|
| [Improve RAG with LOTR ](/examples/Advance_RAG_LOTR/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Advance_RAG_LOTR/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![LLM](https://img.shields.io/badge/openai-api-white)](#)  [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/better-rag-with-lotr-lord-of-retriever-23c8336b9a35)|
| [Advanced RAG: Parent Document Retriever](/examples/parent_document_retriever/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/parent_document_retriever/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![LLM](https://img.shields.io/badge/openai-api-white)](#)  [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/modified-rag-parent-document-bigger-chunk-retriever-62b3d1e79bc6)|
| [Corrective RAG with Langgraph](./tutorials/Corrective-RAG-with_Langgraph/) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/Corrective-RAG-with_Langgraph/CRAG_with_Langgraph.ipynb) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/implementing-corrective-rag-in-the-easiest-way-2/)|
| [Contextual-Compression-with-RAG](/examples/Contextual-Compression-with-RAG/) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Contextual-Compression-with-RAG/main.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#)   [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/enhance-rag-integrate-contextual-compression-and-filtering-for-precision-a29d4a810301/) |
| [Improve RAG with FLARE](./examples/better-rag-FLAIR) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/better-rag-FLAIR/main.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/better-rag-with-active-retrieval-augmented-generation-flare-3b66646e2a9f/) |
| [Agentic RAG ](/tutorials/Agentic_RAG/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/Agentic_RAG/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)|
| [GraphRAG ](/examples/Graphrag/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Graphrag/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/graphrag-hierarchical-approach-to-retrieval-augmented-generation/)|
| [GraphRAG with CSV File ](/tutorials/GraphRAG_CSV/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/GraphRAG_CSV/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://aksdesai1998.medium.com/optimizing-graphrag-with-microsoft-for-csv-data-a-guide-with-lancedb-8e4150b93e37)|
||||

### Vector Search

Build a vector search application using LanceDB for efficient vector-based document retrieval. Input text queries to find the most relevant documents from your corpus.

| Vector Search &nbsp; &nbsp;| Interactive Notebook & Scripts &nbsp; | Blog |
| --------- | -------------------------- | ----------- |
||||
| [Inbuilt Hybrid Search](/examples/Inbuilt-Hybrid-Search) |<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Inbuilt-Hybrid-Search/Inbuilt_Hybrid_Search_with_LanceDB.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#)    [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)||
| [Hybrid search BM25 & lancedb ](./examples/Hybrid_search_bm25_lancedb/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Hybrid_search_bm25_lancedb/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>   [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#) |[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/hybrid-search-combining-bm25-and-semantic-search-for-better-results-with-lan-1358038fe7e6)|
| [NER powered Semantic Search](./tutorials/NER-powered-Semantic-Search) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/NER-powered-Semantic-Search/NER_powered_Semantic_Search_with_LanceDB.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/ner-powered-semantic-search-using-lancedb-51051dc3e493) |
| [Vector Arithmetic with LanceDB](./examples/Vector-Arithmetic-with-LanceDB/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Vector-Arithmetic-with-LanceDB/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>   [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#) |[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/vector-arithmetic-with-lancedb-an-intro-to-vector-embeddings/)|
| [Summarize and Search Reddit Posts](./examples/Reddit-summarization-and-search/) | <a href="https://github.com/lancedb/vectordb-recipes/blob/main/examples/Reddit-summarization-and-search/subreddit_summarization_querying.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>    [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|
| [Imagebind demo app](./examples/imagebind_demo/) | <a href="https://huggingface.co/spaces/raghavd99/imagebind2"><img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo-with-title.svg" alt="hf spaces" style="width: 80px; vertical-align: middle; background-color: white;"></a>  [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|
| [Search Within Images](/examples/search-within-images-with-sam-and-clip/) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/search-within-images-with-sam-and-clip/main.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#)   [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/search-within-an-image-331b54e4285e)|
| [Zero Shot Object Detection with CLIP](./examples/zero-shot-object-detection-CLIP/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/zero-shot-object-detection-CLIP/zero_shot_object_detection_clip.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|
| [Vector Search with TransformersJS](./examples/js-transformers/) |[![JS](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/js-transformers/index.js) [![LLM](https://img.shields.io/badge/local-llm-green)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)|  |
| [Accelerate Vector Search Applications Using OpenVINO](/examples/Accelerate-Vector-Search-Applications-Using-OpenVINO/) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Accelerate-Vector-Search-Applications-Using-OpenVINO/clip_text_image_search.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/accelerate-vector-search-applications-using-openvino-lancedb/)|
||||

### Chatbot

Create a chatbot application using LanceDB for efficient vector-based response generation. Input user queries to retrieve relevant context and generate coherent, context-aware replies.

| Chatbot &nbsp; &nbsp;| Interactive Notebook & Scripts &nbsp; | Blog &nbsp;|
| --------- | -------------------------- | ----------- |
||||
| [Databricks DBRX Website Bot](./examples/databricks_DBRX_website_bot/) | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/databricks_DBRX_website_bot/main.py) [![Databricks LLM](https://img.shields.io/badge/databricks-api-red)](#)    [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|
| [CLI-based SDK Manual Chatbot with Phidata](/examples/CLI-SDK-Manual-Chatbot-Locally/) | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/CLI-SDK-Manual-Chatbot-Locally/assistant.py) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|
| [Youtube transcript search bot](/examples/Youtube-Search-QA-Bot/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Youtube-Search-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/Youtube-Search-QA-Bot/main.py) [![JS](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/Youtube-Search-QA-Bot/index.js) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)||
| [Langchain: Code Docs QA bot](/examples/Code-Documentation-QA-Bot/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Code-Documentation-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/Code-Documentation-QA-Bot/main.py) [![JS](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/Code-Documentation-QA-Bot/index.js) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)||
| [Context-Aware Chatbot using Llama 2 & LanceDB](./tutorials/chatbot_using_Llama2_&_lanceDB) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/chatbot_using_Llama2_&_lanceDB/main.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/context-aware-chatbot-using-llama-2-lancedb-as-vector-database-4d771d95c755) |
||||


### Evaluation

Develop an evaluation application. Input reference and candidate texts to measure their performance on various metrics.

| Evaluation &nbsp; &nbsp;| Interactive Notebook & Scripts &nbsp; | Blog |
| --------- | -------------------------- | ----------- |
||||
| [Evaluating Prompts with Prompttools](/examples/prompttools-eval-prompts/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/prompttools-eval-prompts/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>   [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)|  |
| [Evaluating RAG with RAGAs](./examples/Evaluating_RAG_with_RAGAs/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Evaluating_RAG_with_RAGAs/Evaluating_RAG_with_RAGAs.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>   [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)|  |
||||

### AI Agents

Design an AI agents coordination application with LanceDB for efficient vector-based communication and collaboration. Input queries to enable AI agents to exchange information, coordinate tasks, and achieve shared goals effectively.

| AI Agents &nbsp; &nbsp;| Interactive Notebook & Scripts &nbsp; | Blog |
| --------- | -------------------------- | ----------- |
||||
| [AI email assistant with Composio](/examples/AI-Email-Assistant-with-Composio/) |<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/AI-Email-Assistant-with-Composio/composio-lance.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![LLM](https://img.shields.io/badge/openai-api-white)](#)   [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|
| [AI Trends Searcher with CrewAI](./examples/AI-Trends-with-CrewAI/) |<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/AI-Trends-with-CrewAI/CrewAI_AI_Trends.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![LLM](https://img.shields.io/badge/openai-api-white)](#)    [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/track-ai-trends-crewai-agents-rag/)|
| [SuperAgent Autogen](/examples/SuperAgent_Autogen) |<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/SuperAgent_Autogen/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)||
| [AI Agents: Reducing Hallucination](/examples/reducing_hallucinations_ai_agents/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/reducing_hallucinations_ai_agents/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/reducing_hallucinations_ai_agents/main.py) [![JS](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/reducing_hallucinations_ai_agents/index.js) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#) |[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/how-to-reduce-hallucinations-from-llm-powered-agents-using-long-term-memory-72f262c3cc1f/)|
| [Multi Document Agentic RAG](./examples/multi-document-agentic-rag/) |<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multi-document-agentic-rag/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![LLM](https://img.shields.io/badge/openai-api-white)](#)     [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)|[![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/multi-document-agentic-rag/)|
||||

### Recommender Systems

Create a recommender system application with LanceDB for efficient vector-based item recommendation. Input user preferences or item features to generate personalized recommendations and enhance user experience.

| Recommender Systems | Interactive Notebook & Scripts &nbsp; | Blog |
| --------- | -------------------------- | ----------- |
||||
| [Movie Recommender](/examples/movie-recommender/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/movie-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/movie-recommender/main.py) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|  |
| [Product Recommender](./examples/product-recommender/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/product-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/product-recommender/main.py) [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)| |
| [Arxiv paper recommender](/examples/arxiv-recommender) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/arxiv-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/arxiv-recommender/main.py) [![LLM](https://img.shields.io/badge/local-llm-green)](#)  [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|  |
| [Music Recommender](/applications/Music_Recommandation/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/applications/Music_Recommandation/lancedb_music_recommandation.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)| |||||
||||

### Concepts

Checkout concepts of LLM applications pipeline to ensures accurate information retrieval.

| Concepts | Interactive Notebook | Blog |
| --------- | -------------------------- | ----------- |
|           |                            |             |
| [A Primer on Text Chunking and its Types](./tutorials/different-types-text-chunking-in-RAG) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/different-types-text-chunking-in-RAG/Text_Chunking_on_RAG_application_with_LanceDB.ipynb) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/a-primer-on-text-chunking-and-its-types-a420efc96a13) |
| [Langchain LlamaIndex Chunking](./tutorials/Langchain-LlamaIndex-Chunking) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/Langchain-LlamaIndex-Chunking/Langchain_Llamaindex_chunking.ipynb) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/chunking-techniques-with-langchain-and-llamaindex/) |
| [Create structured dataset using Instructor](./tutorials/NER-dataset-with-Instructor/) | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./tutorials/NER-dataset-with-Instructor/main.py) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)| |
| [Comparing Cohere Rerankers with LanceDB](./tutorials/cohere-reranker) | [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/benchmarking-cohere-reranker-with-lancedb/) |
| [Product Quantization: Compress High Dimensional Vectors](https://blog.lancedb.com/benchmarking-lancedb-92b01032874a-2/) |[![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#) | [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/benchmarking-lancedb-92b01032874a-2/) |
| [LLMs, RAG, & the missing storage layer for AI](https://blog.lancedb.com/llms-rag-the-missing-storage-layer-for-ai-28ded35fa984) | [![intermediate](https://img.shields.io/badge/intermediate-FFDA33)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/llms-rag-the-missing-storage-layer-for-ai-28ded35fa984/) |
| [Fine-Tuning LLM using PEFT & QLoRA](./tutorials/fine-tuning_LLM_with_PEFT_QLoRA) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/fine-tuning_LLM_with_PEFT_QLoRA/main.ipynb) [![local LLM](https://img.shields.io/badge/local-llm-green)](#) [![advanced](https://img.shields.io/badge/advanced-FF3333)](#)| [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/optimizing-llms-a-step-by-step-guide-to-fine-tuning-with-peft-and-qlora-22eddd13d25b) |
| [Extracting Complex tables-text from PDFs using LlamaParse  ](./tutorials/Advace_RAG_LlamaParser) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/Advace_RAG_LlamaParser/main.ipynb) [![LLM](https://img.shields.io/badge/openai-api-white)](#) [![LlamaCloud](https://img.shields.io/badge/Llama-api-pink)](#) [![beginner](https://img.shields.io/badge/beginner-B5FF33)](#)|  |
||||

## Projects & Applications
These are ready to use applications built using LanceDB serverless vector database. You can explore these open source projects, use parts of them in your projects or build your applications on top of these. 

### Node applications powered by LanceDB
| Project Name                                        | Description                                                                                                          | Screenshot                                |
|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| [Writing assistant](https://github.com/lancedb/vectordb-recipes/tree/main/applications/node/lanchain_writing_assistant) | Writing assistant app using lanchain.js with LanceDB, allows you to get real time relevant suggestions and facts based on you written text to help you with your writing.                  | ![Writing assistant](https://github.com/user-attachments/assets/87354e93-df4d-40ad-922b-abcbb62d667c) |


| Project Name                                        | Description                                                                                                          | Screenshot                                |
|-----------------------------------------------------|----------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| [YOLOExplorer](https://github.com/lancedb/yoloexplorer) | Iterate on your YOLO / CV datasets using SQL, Vector semantic search, and more within seconds                  | ![YOLOExplorer](https://github.com/lancedb/vectordb-recipes/assets/15766192/ae513a29-8f15-4e0b-99a1-ccd8272b6131) |
| [Website Chatbot (Deployable Vercel Template)](https://github.com/lancedb/lancedb-vercel-chatbot) | Create a chatbot from the sitemap of any website/docs of your choice. Built using vectorDB serverless native javascript package. | ![Chatbot](assets/vercel-template.gif)    |
| [ Chat with multiple  URL/website  ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/chat_with_anywebsite/) | Conversational AI for Any Website with Mistral,Bge Embedding & LanceDB |![webui_aa](https://github.com/akashAD98/vectordb-recipes/assets/62583018/47a9af87-2d94-4fd8-afa1-373db03bd728)  |
| [ Talk with Podcast ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/talk-with-podcast) | Talk with Youtube Podcast using Ollama and insanely-fast-whisper | ![demo](./assets/talk-with-podcast.gif)|
| [ Hr chatbot  ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/HR_chatbot/) | Hr chatbot - ask your personal query using zero-shot React agent & tools |![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/0ea78428-44be-4bff-874b-79b1fcc3b7d6)|
| [Advanced Chatbot with Parler TTS ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/Chatbot_with_Parler_TTS) | This Chatbot app uses Lancedb Hybrid search, FTS & reranker method with Parlers TTS library.|![image](./assets/chatbot_tts.png)|
| [Multi-Modal Search Engine](https://github.com/lancedb/vectordb-recipes/tree/rf/applications/multimodal-search) | Create a Multi-modal search engine app, to search images using both images or text | ![Search](https://github.com/lancedb/vectordb-recipes/assets/15766192/9805fec8-da72-44c0-be12-ddbe1c2d6afc)|
| [Multimodal Myntra Fashion Search Engine](https://github.com/ishandutta0098/lancedb-multimodal-myntra-fashion-search-engine) | This app uses OpenAI's CLIP to make a search engine that can understand and deal with both written words and pictures.|![image](./assets/myntra-search-engine.png)|
| [Multilingual-RAG](https://github.com/lancedb/vectordb-recipes/tree/main/applications/Multilingual_RAG/) | Multilingual RAG with cohere embedding & support 100+ languages|![image](https://github.com/akashAD98/vectordb-recipes/assets/62583018/be65eb39-25c4-4441-98fc-6ded09689819)|
| [ GTE MLX RAG ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/GTE_mlx_RAG) | mlx based RAG model using lancedb api support | ![image](./assets/rag-mlx.png)|
| [ Healthcare Chatbot  ](https://github.com/lancedb/vectordb-recipes/tree/main/applications/Healthcare_chatbot/) | Healthcare chatbot using domain specific LLM  & Embedding model | ![image](./assets/chatbot_medical.png)|
||||



**🌟 New! 🌟 Applied GenAI and VectorDB course on Udacity**
Learn about GenAI and vectorDBs using LanceDB in the recently launched [Udacity Course](https://www.udacity.com/course/building-generative-ai-solutions-with-vector-databases--cd12952)


<img src="./assets/udacity-course.png" width="80%" height="80%" />


## Contributing Examples
If you're working on some cool applications that you'd like to add to this repo, please open a PR!
