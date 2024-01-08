# Modified RAG: Parent Document & Bigger chunk Retriever
To get around the problem of larger size of Parent document, what you can do right now is to make bigger chunks along with smaller ones. For example, if your smaller chunks are of 512 tokens and your Parent Documents are of 2048 tokens on average, you can make chunks of size 1024. Now during retrieval, it’ll match as the previous one above BUT this time, instead of parent document, it’ll fetch the Bigger chunk and pass it to LLM. this way you’ll lose some text for sure but not completely. You could use use 2 verses instead of original 4 to make the model understand the writing style, context etc etc that too being within the limits. Good thing, you just have to change 1 line from the previous one.
<br>

Colab walkthrough - <a href="https://github.com/lancedb/vectordb-recipes/blob/main/examples/parent_document_retriever/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

[Read full blog](https://blog.lancedb.com/modified-rag-parent-document-bigger-chunk-retriever-62b3d1e79bc6)

