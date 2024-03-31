<a href="https://github.com/lancedb/vectordb-recipes/blob/main/examples/parent_document_retriever/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

# Modified RAG: Parent Document & Bigger chunk Retriever
There are some cases when your users want to have a task done by providing just a couple of lines input or even worse, couple of words. In this example, let’s say I have a “Sequel” song generation task given a line or two as input. Now if it’s a Part-2 of something, the tone, writing style, story etc are supposed to be related to the previous song so given the line “I am whatever I am”, my LLM should generate something related to the previous song not a mixture of 10 different songs and artists. If you use a vanilla RAG here, you’d be getting multiple results which might not be from same song, artist or even genre. If you use only the first match, you lose a lot of context as a smaller chunk won’t give the full context of the song.

### Solution 
There are 2 approaches to tackle that. Let’s go one by one from theory to code starting from **Parent Document Retriever**.


<a href="https://github.com/lancedb/vectordb-recipes/blob/main/examples/parent_document_retriever/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

[Read full blog](https://blog.lancedb.com/modified-rag-parent-document-bigger-chunk-retriever-62b3d1e79bc6)

