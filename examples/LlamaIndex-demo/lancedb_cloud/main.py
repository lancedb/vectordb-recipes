from datetime import datetime
import openai
import requests
import os

from llama_index.core import SimpleDirectoryReader,Document, StorageContext
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.lancedb import LanceDBVectorStore
import textwrap

if __name__ == "__main__":
    if "OPENAI_API_KEY" not in os.environ:
        raise ValueError("OPENAI_API_KEY environment variable not set. Please set it")
    else:
        openai.api_key = os.environ["OPENAI_API_KEY"]

    # Download the document
    data_path = r"data/paul_graham/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    url = "https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt"
    r = requests.get(url)
    with open(data_path + "/paul_graham_essay.txt", "wb") as f:
        f.write(r.content)

    # Load the document
    documents = SimpleDirectoryReader(data_path).load_data()
    print("Document ID:", documents[0].doc_id, "Document Hash:", documents[0].hash)

    # Create a LanceDBVectorStore and create an index
    vector_store = LanceDBVectorStore(
        uri="db://your-project-slug",  # your remote DB URI
        api_key="sk_...",  # lancedb cloud api key
        region="us-east-1",  # the region you configured
    )

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    # Query via MetadataFilters
    from llama_index.core.vector_stores import (
        MetadataFilters,
        FilterOperator,
        FilterCondition,
        MetadataFilter,
    )

    date = datetime.today().strftime("%Y-%m-%d")
    query_filters = MetadataFilters(
        filters=[
            MetadataFilter(key="creation_date", operator=FilterOperator.EQ, value=date),
            MetadataFilter(key="file_size", value=75040, operator=FilterOperator.GT),
        ],
        condition=FilterCondition.AND,
    )

    query_engine = index.as_query_engine(
        filters=query_filters,
    )

    response = query_engine.query("How much did Viaweb charge per month?")
    print("==== query via MetadataFilters")
    print(response)
    print("metadata -", response.metadata)

    # Query via LanceDB where clause
    lance_filter = "metadata.file_name = 'paul_graham_essay.txt' "
    retriever = index.as_retriever(vector_store_kwargs={"where": lance_filter})
    response = retriever.retrieve("What did the author do growing up?")
    print("==== query via LanceDB where clause")
    print(response[0].get_content())
    print("metadata -", response[0].metadata)

    # add data to an existing index and query with the new data
    del index

    index = VectorStoreIndex.from_documents(
        [Document(text="The sky is purple in Portland, Maine")],
        uri="/tmp/new_dataset",
    )
    query_engine = index.as_query_engine()
    response = query_engine.query("Where is the sky purple?")
    print("==== query with new data")
    print(textwrap.fill(str(response), 100))
