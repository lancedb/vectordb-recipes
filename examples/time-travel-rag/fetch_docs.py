import requests
from typing import List, Dict, Any
import config


def fetch_documents(publication_date: str, per_page: int = 5) -> List[Dict[str, Any]]:
    print(
        f"\nFetching {per_page} documents for publication date: {publication_date}..."
    )

    params = {
        "per_page": per_page,
        "fields[]": config.API_FIELDS,
        "conditions[publication_date][is]": publication_date,
    }

    try:
        response = requests.get(config.FEDERAL_REGISTER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get("results"):
            print(f"Successfully fetched {len(data['results'])} documents.")
            return data["results"]
        else:
            print("No results found for this date.")
            return []

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Federal Register API: {e}")
        return []
    except KeyError:
        print("API response format is unexpected. 'results' key not found.")
        return []
