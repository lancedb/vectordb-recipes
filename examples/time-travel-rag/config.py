
DB_URI = "./lancedb"
TABLE_NAME = "federal_register"
EXPERIMENTAL_TABLE_NAME = f"{TABLE_NAME}_experimental"

PRODUCTION_MODEL = "all-MiniLM-L6-v2"
EXPERIMENTAL_MODEL = "all-mpnet-base-v2"

FEDERAL_REGISTER_API_URL = "https://www.federalregister.gov/api/v1/documents.json"
API_FIELDS = ["title", "abstract", "publication_date", "html_url", "document_number"]


REPRODUCIBLE_START_DATE = "2024-08-18"
