# 🔍Search engine using SAM & CLIP

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/search-within-images-with-sam-and-clip/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white)](https://medium.com/etoai/search-within-an-image-331b54e4285e)
![“A Dog”](https://github.com/kaushal07wick/vectordb-recipes/assets/57106063/3907c1e5-009b-4ffb-8ea2-2eddb58f3346)

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

 Read the Full blog post on **Medium**
