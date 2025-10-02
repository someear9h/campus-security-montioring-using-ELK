from elasticsearch import Elasticsearch
from typing import Optional, Dict, Any
from schemas.entity_profile import EntityProfile

# --- ELASTICSEARCH CONNECTION ---
# This client will be reused across all functions in this service.
try:
    es_client = Elasticsearch("http://localhost:9201")
    if not es_client.ping():
        raise ConnectionError("Initial connection to Elasticsearch failed.")
except Exception as e:
    es_client = None
    print(f"WARNING: Could not connect to Elasticsearch. Entity service will be disabled. {e}")

# --- SERVICE FUNCTIONS ---

def find_profile_by_identifier(
    id_column: str,
    id_value: str
) -> Optional[EntityProfile]:
    """
    Finds a single entity profile from Elasticsearch using any known identifier.

    Args:
        id_column (str): The field to search in (e.g., 'card_id', 'email').
        id_value (str): The value to search for (e.g., 'C7151').

    Returns:
        Optional[EntityProfile]: A Pydantic model of the profile if found,
                                 otherwise None.
    """
    if not es_client:
        print("ERROR: Elasticsearch client not available.")
        return None

    # Elasticsearch query DSL: We use a 'term' query for an exact match.
    # We search in the field specified by `id_column`.
    query = {
        "query": {
            "term": {
                # We add ".keyword" to search the non-analyzed version of the field
                # for an exact match, which is crucial for IDs.
                f"{id_column}.keyword": id_value
            }
        }
    }

    try:
        response = es_client.search(index="entities", body=query)
        hits = response["hits"]["hits"]

        # If we found at least one match, we take the first one.
        if hits:
            # The actual data is in the '_source' field of the hit.
            profile_data = hits[0]["_source"]
            # We validate and parse this data using our Pydantic model.
            return EntityProfile(**profile_data)

    except Exception as e:
        print(f"ERROR: An error occurred while searching Elasticsearch: {e}")
        return None

    # If no match was found, return None.
    return None
