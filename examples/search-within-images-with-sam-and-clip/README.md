# 🔍Search engine using SAM & CLIP

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/search-within-images-with-sam-and-clip/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>  [![Ghost](https://img.shields.io/badge/ghost-000?style=for-the-badge&logo=ghost&logoColor=%23F7DF1E)](https://blog.lancedb.com/search-within-an-image-331b54e4285e)
![“A Dog”](../../assets/search-within-image.png)

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


![“A Dog”](../../assets/search-within-image-flow.png)
 Read the Full [blog post](https://blog.lancedb.com/search-within-an-image-331b54e4285e)
