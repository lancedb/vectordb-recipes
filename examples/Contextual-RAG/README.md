## Improve RAG with Contextual Retrieval

<a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/Contextual-RAG/Anthropic_Contextual_RAG.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>

In traditional RAG, a basic chunking method creates vector embeddings for each chunk separately, and RAG systems use these embeddings to find chunks that match the query. However, this approach has a problem: it loses the context of the original document. 
In the past, several methods have been proposed to improve retrieval using context. These include adding generic document summaries to chunks,  Hypothetical Document Embedding (HyDE), and summary-based indexing.

**Contextual Embeddings** address this issue by incorporating relevant context and prepending it into each chunk before creating embeddings. This approach enhances the quality of each embedded chunk, leading to more accurate retrieval and improved overall performance. On average, across all the data sources we tested, Contextual Embeddings reduced the failure rate for retrieving the top 20 chunks by 35%.

In this example, we'll explore Contextual Retrieval, a technique to improve the accuracy of vector search by providing additional context for the chunks of a document, by inputting both the document and the chunk to an LLM and asking it to provide a succinct context for the chunk within the document.

This is a way to combat the lost context problem that occurs in chunking, e.g., if a text is split into sentences, the context of later sentences as they relate to earlier sentences is lost.

The idea here is to do these things:
1. For each document, make chunks (Nothing new. Just like Vanilla RAG)
2. For each Chunk you created, as an LLM create a context of that Chunk (You see this is new!)
3. Append that context to the original chunk
4. Create BM-25 and Vector Index based on those chunks for Hybrid Search (New to you? See this amazing blog by LanceDB on hybrid search)
5. Search as usual!