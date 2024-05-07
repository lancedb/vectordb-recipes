import time
from tqdm import tqdm

import pandas as pd

from llama_index.core import SimpleDirectoryReader
from llama_index.core.llama_dataset import LabelledRagDataset
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import SimpleDirectoryReader, ServiceContext, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import TextNode, NodeRelationship, RelatedNodeInfo
from llama_index.embeddings.openai import OpenAIEmbedding
from lancedb.rerankers import CohereReranker, ColbertReranker


def evaluate(
    docs,
    dataset,
    embed_model=None,
    reranker=None,
    top_k=5,
    query_type="auto",
    verbose=False,
):
    #corpus = dataset['corpus']
    #queries = dataset['queries']
    #relevant_docs = dataset['relevant_docs']

    vector_store = LanceDBVectorStore(uri=f"/tmp/lancedb_cohere-bench-{time.time()}")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    service_context = ServiceContext.from_defaults(embed_model=embed_model)
    index = VectorStoreIndex.from_documents(
        docs,
        service_context=service_context, 
        show_progress=True,
        storage_context=storage_context,
    )
    tbl = vector_store._connection.open_table(vector_store.table_name)
    tbl.create_fts_index("text", replace=True)

    eval_results = []
    ds = dataset.to_pandas()
    for idx in tqdm(range(len(ds))):
        query = ds['query'][idx]
        reference_context = ds['reference_contexts'][idx]
        query_vector = embed_model.get_query_embedding(query)
        try:
            if reranker is None:
                rs = tbl.search(query_vector).limit(top_k).to_pandas()
            elif query_type == "auto":
                rs = tbl.search((query_vector, query)).rerank(reranker=reranker).limit(top_k).to_pandas()
            elif query_type == "vector":
                rs = tbl.search(query_vector).rerank(reranker=reranker, query_string=query).limit(top_k*2).to_pandas() # Overfetch for vector only reranking
        except Exception as e:
            print(f'Error with query: {idx} {e}')
            continue
        retrieved_texts = rs['text'].tolist()[:top_k]
        expected_text = reference_context[0]
        is_hit = expected_text in retrieved_texts  # assume 1 relevant doc
        eval_result = {
            'is_hit': is_hit,
            'retrieved': retrieved_texts,
            'expected': expected_text,
            'query': query,
        }
        eval_results.append(eval_result)
    return eval_results

rag_dataset = LabelledRagDataset.from_json("./data/rag_dataset.json")
documents = SimpleDirectoryReader(input_dir="./data/source_files").load_data()

embed_models = {
"bge": HuggingFaceEmbedding(model_name="BAAI/bge-large-en-v1.5"),
"colbert": HuggingFaceEmbedding(model_name="colbert-ir/colbertv2.0")
}
rerankers = {
    "None": None,
    "cohere-v2": CohereReranker(),
    "cohere-v3": CohereReranker(model_name="rerank-english-v3.0"),
    "ColbertReranker": ColbertReranker(),
}

scores = {}
for embed_name, embed_model in embed_models.items():
    for reranker_name, reranker in rerankers.items():
        eval_results = evaluate(
            docs=documents,
            dataset=rag_dataset,
            embed_model=embed_model,
            reranker=reranker,
            top_k=5,
            verbose=True,
        )
        print(f" Embedder {embed_name} Reranker: {reranker_name}")
        score = pd.DataFrame(eval_results)['is_hit'].mean()
        print(score)
        scores[reranker_name] = score

        if reranker_name != "None":
            eval_results = evaluate(
                docs=documents,
                dataset=rag_dataset,
                embed_model=embed_model,
                reranker=reranker,
                top_k=5,
                query_type="vector",
                verbose=True,
            )
            print(f"Embedder {embed_name} Reranker: {reranker_name} (vector)")
            score = pd.DataFrame(eval_results)['is_hit'].mean()
            print(score)
            scores[f"{reranker_name}_vector"] = score
