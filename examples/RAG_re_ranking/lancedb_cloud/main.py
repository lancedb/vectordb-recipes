from FlagEmbedding import LLMEmbedder, FlagReranker 
import lancedb
import re
import pandas as pd
import random

from datasets import load_dataset

import torch
import gc

from lancedb.embeddings import with_embeddings

embed_model = LLMEmbedder('BAAI/llm-embedder', use_fp16=False) # Load model (automatically use GPUs)
reranker_model = FlagReranker('BAAI/bge-reranker-base', use_fp16=True) # use_fp16 speeds up computation with a slight performance degradation
task = "qa" # Encode for a specific task (qa, icl, chat, lrlm, tool, convsearch)
# get embedding using LLM embedder
def embed_documents(batch):
    """
    Function to embed the whole text data
    """
    return embed_model.encode_keys(batch, task=task) # Encode data or 'keys'

def search(table, query, top_k = 10):
  """
  Search a query from the table
  """
  query_vector = embed_model.encode_queries(query, task=task) # Encode the QUERY (it is done differently than the 'key')
  search_results = table.search(query_vector).limit(top_k)
  return search_results

def rerank(query, search_results):
  search_results["old_similarity_rank"] = search_results.index+1 # Old ranks

  torch.cuda.empty_cache()
  gc.collect()

  search_results["new_scores"] = reranker_model.compute_score([[query,chunk] for chunk in search_results["text"]]) # Re compute ranks
  return search_results.sort_values(by = "new_scores", ascending = False).reset_index(drop = True)

def main():   
   queries = load_dataset("BeIR/scidocs", "queries")["queries"].to_pandas()
   docs = load_dataset('BeIR/scidocs', 'corpus')["corpus"].to_pandas().dropna(subset = "text").sample(10000) # just random samples for faster embed demo
    
   # create Database using LanceDB Cloud
   uri = "db://your-project-slug"
   api_key = "sk_..."
   db = lancedb.connect(uri, api_key=api_key, region="us-east-1")
   table_name = "doc_embed"
   try:
    # Use the train text chunk data to save embed in the DB
    data = with_embeddings(embed_documents, docs, column = 'text',show_progress = True, batch_size = 128)
    table = db.create_table(table_name, data=data) # create Table
   except:
    table = db.open_table(table_name) # Open Table

    query = random.choice(queries["text"])
    print("QUERY:-> ", query)

    # get top_k search results
    search_results = search(table, "what is mitochondria?", top_k = 10).to_pandas().dropna(subset = "text").reset_index(drop = True)
    print("SEARCH RESULTS:-> ", search_results)

    # Rerank search results using Reranker from BGE Reranker
    print("QUERY:-> ", query)
    search_results_reranked = rerank(query, search_results)
    print("SEARCH RESULTS RERANKED:-> ", search_results_reranked)

if __name__ == "__main__":
    main()