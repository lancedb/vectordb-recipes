# 🔍Search engine using SAM & CLIP

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Search-Engine-with-SAM-and-CLIP/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://blog.lancedb.com/context-aware-chatbot-using-llama-2-lancedb-as-vector-database-4d771d95c755)


###   🚀Create a Search Engine within an Image use **SAM**(Segment Anything) and **CLIP** (Constrastive Language Image Pretraining) model.
Follow the Colab Notebook for full code.

## Interface 🌟

1. Load the model.
2. Create the Segmentation mask of any Image.
3. Get the Embeddings of each extracted Segmentation masks as an seperate image.
4. Embed the User Query.
5. Index the Image embeddings into **LanceDB**.
6. Use Search method to find the closest match of Image Embedding (particular Segmentation Mask) and User Query.
7. Output the Highlighted closest object present.

 Read the Full blog post on **Medium**.