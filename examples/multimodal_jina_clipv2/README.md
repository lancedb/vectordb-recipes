# Multimodal Search Engine with Jina-CLIP v2 and LanceDB

Welcome to the **Multimodal Search Engine** project! This project utilizes [Jina-CLIP v2](https://jina.ai/news/jina-clip-v2-multilingual-multimodal-embeddings-for-text-and-images/) and [LanceDB](https://lancedb.dev) 
to enable robust search functionality across both text and image data in 89 languages.

---

## Features

- **Multimodal Search**: Search across both image and text inputs.
- **Multilingual Support**: Supports 89 languages for text queries and captions.
- **Efficient Retrieval**: Powered by [LanceDB](https://lancedb.dev), ensuring low latency and high throughput.
- **Matryoshka Representations**: Enables hierarchical embedding structures for fine-grained similarity.

---

### How It Works
- Input: Accepts either a text query or an image as input.
- Encoding: Uses Jina-CLIP v2 to convert text and images into a shared embedding space.
- Storage: Stores these embeddings in LanceDB for efficient retrieval.
- Search: Matches queries to the most relevant embeddings in the database and returns results.

---

## code 

 Colab walkthrough   <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_jina_clipv2/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

 ---
