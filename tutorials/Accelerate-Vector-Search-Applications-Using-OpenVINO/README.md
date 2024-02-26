[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/Accelerate-Vector-Search-Applications-Using-OpenVINO/clip_text_image_search.ipynb)

## Accelerate vector search Applications using OpenVINO

**CLIP from OpenAI for Text-to-Image and Image-to-Image searching** and we’ll also do a comparative analysis of the Pytorch model, FP16 OpenVINO format, and INT8 OpenVINO format in terms of speedup.

Here are a few Key points converted in this article.

Text-to-Image and Image-to-Image Search using CLIP

- Using the HuggingFace model
- Using OpenVINO conversion to speed up by **70%**
- Using Quantization with OpenVINO NNCF to speed up by **400%**

**These Results are on 13th Gen Intel(R) Core(TM) i5–13420H using OpenVINO=2023.2 and NNCF=2.7.0 version.**

[Read More in Blog](https://blog.lancedb.com/accelerate-vector-search-applications-using-openvino-51366eabf866)