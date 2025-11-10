import config
import fetch_docs
import embed_ingest
from datetime import datetime, timedelta
import textwrap
import pandas as pd
import os
import shutil
import lancedb


def find_next_publication_date(start_date_str: str, max_days_to_search: int = 7):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    for i in range(1, max_days_to_search + 1):
        check_date = start_date + timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        docs = fetch_docs.fetch_documents(date_str, per_page=500)
        if docs:
            return date_str, docs
    return None, []


def print_search_result(result_df: pd.DataFrame, version: str):
    print(f"--- Top Result for Version: {version} ---")
    if result_df.empty:
        print("No results found for this version.")
        return

    top_result = result_df.iloc[0]
    print(f"📄 Title: {top_result['title']}")
    print(f"🗓️  Date: {top_result['publication_date']}")
    print(f"📏 Distance: {top_result['_distance']:.4f}")

    abstract = top_result.get("abstract") or "[No abstract available for this document]"

    print(f"📝 Abstract:{textwrap.fill(abstract, width=100)}")


def run_workflow():
    print("--- Initializing Database Environment ---")
    if os.path.exists(config.DB_URI):
        shutil.rmtree(config.DB_URI)
        print(f"Removed old database at {config.DB_URI}")
    os.makedirs(config.DB_URI, exist_ok=True)
    db = lancedb.connect(config.DB_URI)

    prod_model = embed_ingest.get_embedding_model(config.PRODUCTION_MODEL)

    print("\n--- STEP 1: Initial Data Ingestion ---")
    initial_docs = []
    last_publication_date = config.REPRODUCIBLE_START_DATE

    last_publication_date, initial_docs = find_next_publication_date(
        last_publication_date
    )
    if not initial_docs:
        print("Failed to fetch any data to create an initial table. Exiting.")
        return

    initial_data = embed_ingest.embed_documents(prod_model, initial_docs)

    print(f"\nCreating table '{config.TABLE_NAME}'...")
    tbl = db.create_table(config.TABLE_NAME, data=initial_data)
    print(
        f"✅ Table '{config.TABLE_NAME}' created. Version: {tbl.version}, Rows: {len(tbl)}"
    )

    print("\n--- STEP 2: Simulating Sequential Daily Updates ---")

    last_publication_date, update_docs_1 = find_next_publication_date(
        last_publication_date
    )
    if update_docs_1:
        update_data_1 = embed_ingest.embed_documents(prod_model, update_docs_1)
        tbl.add(update_data_1)
        print(
            f"✅ Data added to '{tbl.name}'. New Version: {tbl.version}, Total Rows: {len(tbl)}"
        )

    last_publication_date, update_docs_2 = find_next_publication_date(
        last_publication_date
    )
    if update_docs_2:
        update_data_2 = embed_ingest.embed_documents(prod_model, update_docs_2)
        tbl.add(update_data_2)
        print(
            f"✅ Data added to '{tbl.name}'. New Version: {tbl.version}, Total Rows: {len(tbl)}"
        )

    print("\n========================================================")
    print("= PART 1: AUDITING KNOWLEDGE BASE ACROSS TIME  =")
    print("========================================================")

    query_text = "cybersecurity reporting requirements for public companies"
    print(f"\nRunning audit for query: '{query_text}'")
    query_vector = prod_model.encode(query_text)

    for version_num in range(1, tbl.version + 1):
        tbl_to_search = db.open_table(config.TABLE_NAME)
        tbl_to_search.checkout(version_num)
        print(
            f"✅ Successfully checked out Version {version_num} of '{config.TABLE_NAME}'. Total rows: {len(tbl_to_search)}"
        )

        if tbl_to_search:
            print(
                f"\nQuerying table '{tbl_to_search.name}' (Version {tbl_to_search.version})..."
            )
            search_results = tbl_to_search.search(query_vector).limit(1).to_pandas()
            print_search_result(
                search_results, f"V{version_num} ({config.PRODUCTION_MODEL})"
            )

    print(
        "\n✅ Date-based audit complete. Results show how knowledge evolves over time."
    )

    print("\n=============================================================")
    print("= PART 2: A/B TESTING DIFFERENT EMBEDDING MODELS  =")
    print("=============================================================")

    exp_model = embed_ingest.get_embedding_model(config.EXPERIMENTAL_MODEL)

    db.drop_table(config.EXPERIMENTAL_TABLE_NAME, ignore_missing=True)

    print(f"\nCreating table '{config.EXPERIMENTAL_TABLE_NAME}'...")
    exp_tbl = db.create_table(
        config.EXPERIMENTAL_TABLE_NAME,
        data=embed_ingest.embed_documents(
            exp_model, tbl.to_pandas().to_dict("records")
        ),
    )
    print(
        f"✅ Table '{config.EXPERIMENTAL_TABLE_NAME}' created. Version: {exp_tbl.version}, Rows: {len(exp_tbl)}"
    )

    if exp_tbl:
        print("\nComparing search results for the same data with different models:")

        print(f"\nQuerying table '{tbl.name}' (Version {tbl.version})...")
        print_search_result(
            tbl.search(query_vector).limit(1).to_pandas(),
            f"Latest Prod V{tbl.version} ({config.PRODUCTION_MODEL})",
        )

        print(f"\nQuerying table '{exp_tbl.name}' (Version {exp_tbl.version})...")
        print_search_result(
            exp_tbl.search(exp_model.encode(query_text)).limit(1).to_pandas(),
            f"Experimental ({config.EXPERIMENTAL_MODEL})",
        )

    print(
        "\n✅ A/B test complete. Notice the difference in relevance (distance score) between models."
    )


if __name__ == "__main__":
    run_workflow()
