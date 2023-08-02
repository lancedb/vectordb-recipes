# VectorDB-recipes
Example Applications

| Example | Interactive Envs | Scripts  |
|-------- | ---------------- | ------   |
| | | |
| [Youtube transcript search bot](./examples/youtube_bot/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/youtube_bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/youtube_bot/main.py)  [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/youtube_bot/index.js)|
| [Langchain: Code Docs QA bot](./examples/Code-Documentation-QA-Bot/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Code-Documentation-QA-Bot/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/Code-Documentation-QA-Bot/main.py)  [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/Code-Documentation-QA-Bot/index.js)|
| [AI Agents: Reducing Hallucination](./examples/reducing_hallucinations_ai_agents/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/reducing_hallucinations_ai_agents/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/reducing_hallucinations_ai_agents/main.py)  [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/reducing_hallucinations_ai_agents/index.js)|
| [Multimodal CLIP: DiffusionDB](./examples/multimodal_clip/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/multimodal_clip/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>| [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/multimodal_clip/main.py)  |
| [TransformersJS Embedding example](./examples/js-transformers/) | | [![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)](./examples/js-transformers/index.js)  |
| [Movie Recommender](./examples/movie-recommender/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/movie-recommender/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/movie-recommender/main.py)  |
| [Audio Search](./examples/audio_search/) | <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/audio_search/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a> | [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](./examples/audio_search/main.py)  |

## Setup
### Quickstart
Install python and javascript dependencies for all examples. Some examples might have extra folder level dependencies.
```bash
pip install -r requirements.txt
```
```bas
npm i
```

## Projects Gallery
Some real-world vectordb projects and packages
### [YOLOExplorer](https://github.com/lancedb/yoloexplorer)
YOLOExplorer : Iterate on your YOLO / CV datasets using SQL, Vector semantic search, and more within seconds
![dash_intro](https://github.com/lancedb/vectordb-recipes/assets/15766192/ae513a29-8f15-4e0b-99a1-ccd8272b6131)

## Developing Examples

Create a new folder with either a `main.py` or `index.js` file. If you are writing solely in python, be sure also include a `main.ipynb`
file that walks through your example. Additionally, please include `test.py` file that include `pytest` unit tests for your functions (or main). Take a look at some of the other examples, and please mock your api calls using `pytest`. If you are writing api calls in javascript, add to the files ignored
within the `compile_testing.js` file in the root directory.

If you require a dataset to be downloaded before you can run either files, please include bash script within your `test.py` file, like this:

```bash
subprocess.Popen("wget dataset.zip", shell=True).wait()
```