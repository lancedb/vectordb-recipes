# Load data
import argparse
from llama_index.core import VectorStoreIndex, Settings, StorageContext
from llama_index.readers.web import SimpleWebPageReader
from llama_index.vector_stores.lancedb import LanceDBVectorStore
from llama_index.llms.databricks import Databricks
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from gen_image import load_models, generate_image, RESPONSE_TO_DIFFUSER_PROMPT

MODEL, STEPS = None, None


def get_doc_from_url(url):
    documents = SimpleWebPageReader(html_to_text=True).load_data([url])
    return documents


def build_RAG(
    url="https://harrypotter.fandom.com/wiki/Hogwarts_School_of_Witchcraft_and_Wizardry",
    embed_model="mixedbread-ai/mxbai-embed-large-v1",
    uri="~/tmp/lancedb_hogwart",
    force_create_embeddings=False,
    illustrate=True,
    diffuser_model="sdxl",
):
    Settings.embed_model = HuggingFaceEmbedding(model_name=embed_model)
    Settings.llm = Databricks(model="databricks-dbrx-instruct")
    if illustrate:
        print("Loading sdxl model")
        model, steps = load_models(diffuser_model)
        # This is a hack to tradeoff between speed and quality
        steps = 1
        print("Model loaded")
    documents = get_doc_from_url(url)
    vector_store = LanceDBVectorStore(uri=uri)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    query_engine = index.as_chat_engine()

    return query_engine, model, steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build RAG system")
    parser.add_argument(
        "--url",
        type=str,
        default="https://harrypotter.fandom.com/wiki/Hogwarts_School_of_Witchcraft_and_Wizardry",
        help="URL of the document",
    )
    parser.add_argument(
        "--embed_model",
        type=str,
        default="mixedbread-ai/mxbai-embed-large-v1",
        help="Embedding model",
    )
    parser.add_argument(
        "--uri",
        type=str,
        default="~/tmp/lancedb_hogwarts_12",
        help="URI of the vector store",
    )
    parser.add_argument(
        "--force_create_embeddings",
        type=bool,
        default=False,
        help="Force create embeddings",
    )
    parser.add_argument(
        "--diffuser_model",
        type=str,
        default="sdxl",
        help="Model ID",
    )

    parser.add_argument(
        "--illustrate",
        type=bool,
        default=True,
        help="Annotate",
    )
    args = parser.parse_args()
    # hardcode model because no one should use sd
    args.diffuser_model = "sdxl"
    query_engine, model, steps = build_RAG(
        args.url,
        args.embed_model,
        args.uri,
        args.force_create_embeddings,
        args.illustrate,
        args.diffuser_model,
    )

    print("Ask a question relevant to the given context:")
    while True:
        query = input()
        response = query_engine.chat(query)
        print(response)
        print("\n Illustrating the response...:")
        image = generate_image(
            model,
            steps,
            Settings.llm.complete(
                RESPONSE_TO_DIFFUSER_PROMPT.format(str(response.response))
            ).text,
        )
        image.show()
