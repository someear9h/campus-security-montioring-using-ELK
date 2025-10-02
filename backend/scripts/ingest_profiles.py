"""
This file's only job is to read your student or staff profiles.csv,
format the data, and push it into a new Elasticsearch index called entities
"""
import sys
from pathlib import Path

# 1. Get the path to the directory containing this script ('.../backend/scripts/').
SCRIPT_DIR = Path(__file__).resolve().parent
# 2. Get the path to the project's root directory ('.../backend/').
PROJECT_ROOT = SCRIPT_DIR.parent
# 3. Add the project root to Python's search path.
sys.path.append(str(PROJECT_ROOT))

import os
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

# --- CONFIGURATION ---
PROFILES_CSV_PATH = PROJECT_ROOT / "data" / "student or staff profiles.csv"

# Read the host from an environment variable, defaulting to port 9201.
ES_HOST = os.getenv("ELASTICSEARCH_HOSTS", "http://localhost:9201")
ES_INDEX_NAME = "entities"


# --- MAIN SCRIPT LOGIC ---
def ingest_entity_profiles():
    """
    Reads the profiles CSV, prepares the data, and bulk-ingests it
    into the 'entities' Elasticsearch index.
    """
    print("--- Starting Entity Profile Ingestion ---")

    # 1. Connect to Elasticsearch
    try:
        es_client = Elasticsearch(ES_HOST)
        if not es_client.ping():
            raise ConnectionError("Could not connect to Elasticsearch.")
        print("Successfully connected to Elasticsearch.")
    except Exception as e:
        print(f"FATAL ERROR: Could not connect to Elasticsearch at {ES_HOST}. {e}")
        return

    # 2. Read and clean the CSV data using pandas
    try:
        df = pd.read_csv(PROFILES_CSV_PATH)
        df = df.where(pd.notnull(df), None)
        print(f"Successfully loaded {len(df)} profiles from '{PROFILES_CSV_PATH}'.")
    except FileNotFoundError:
        print(f"FATAL ERROR: The profiles file was not found at '{PROFILES_CSV_PATH}'.")
        return

    # 3. Prepare the data for bulk ingestion
    actions = [
        {
            "_index": ES_INDEX_NAME,
            "_source": record
        }
        for record in df.to_dict(orient="records")
    ]
    print(f"Prepared {len(actions)} documents for ingestion.")

    # 4. Perform the bulk ingest
    try:
        if es_client.indices.exists(index=ES_INDEX_NAME):
            print(f"Deleting existing index '{ES_INDEX_NAME}'...")
            es_client.indices.delete(index=ES_INDEX_NAME)
        print(f"Ingesting documents into '{ES_INDEX_NAME}'...")
        success, failed = bulk(es_client, actions)
        print(f"--- Ingestion Complete ---")
        print(f"Successfully indexed {success} documents.")
        if failed:
            print(f"Failed to index {len(failed)} documents.")
    except Exception as e:
        print(f"FATAL ERROR: An error occurred during bulk ingestion: {e}")


if __name__ == "__main__":
    ingest_entity_profiles()
