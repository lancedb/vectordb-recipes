[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/tutorials/different-types-text-chunking-in-RAG/Text_Chunking_on_RAG_application_with_LanceDB.ipynb)

## Why is Text Chunking Important?
There are various reasons why Text Chunking becomes important when working with LLMs, we’ll share a few of them which have a significant impact on the results.

Let's try to understand it with an example. You have a document of 15 pages full of text and you want to perform summarization and Question Answering on the document for which the first and foremost step is to extract embeddings of the full document, now from here all the problems start with which are listed.

If you are extracting embeddings of a whole document in one go, it takes the context of the whole document and it can lose lots of valuable information about specific topics, which will result in precise and missed information for LLMs.
If you are using any model provider like OpenAI, you have to be mindful of chunk size because GPT4 comes with a 32K window size, which does not cause any issue but still it's good to be mindful from starting.
Failing to use Text Chunking in right way when needed can lead to issues that affect the overall quality and accessibility of the text.

These are the main two reasons why Text Chunking because important instead of using big documents directly.

[Read More](https://blog.lancedb.com/a-primer-on-text-chunking-and-its-types-a420efc96a13)