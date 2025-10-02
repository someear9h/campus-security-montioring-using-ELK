import pandas as pd
import requests
import time
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / "data" / "campus_card_swipes.csv"

# API endpoints
API_URL = "http://127.0.0.1:8000/card-swipes/ingest"
LOG_URL = "http://127.0.0.1:5045"  # Logstash endpoint


def simulate_real_time_swipes():
    """
    Reads historical swipe data from a CSV, sorts it by time,
    sends it to FastAPI, and also logs to Logstash.
    """
    print("--- Starting Real-Time Data Simulation ---")

    try:
        # Load historical data
        df = pd.read_csv(CSV_PATH)
        print(f"Loaded {len(df)} records from '{CSV_PATH}'.")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except FileNotFoundError:
        print(f"FATAL ERROR: File not found at '{CSV_PATH}'.")
        return

    # Sort events chronologically
    df.sort_values(by='timestamp', inplace=True)
    print("Swipe records sorted by timestamp.")

    print("\n--- Sending swipe data ---")
    for _, row in df.iterrows():
        payload = {
            "card_id": row['card_id'],
            "location_id": row['location_id'],
            "timestamp": row['timestamp'].isoformat()
        }

        # Send to FastAPI
        try:
            response = requests.post(API_URL, json=payload)
            status = "success" if response.status_code in [200, 201] else "failed"

            if status == "success":
                print(f"SUCCESS: {payload['card_id']} -> {payload['location_id']}")
            else:
                print(f"FAILURE: {response.status_code}, {response.text}")

        except requests.exceptions.ConnectionError:
            print(f"\nFATAL ERROR: Could not connect to {API_URL}. Is FastAPI running?")
            return

        # Log event to Logstash
        log_event = {
            "timestamp": datetime.datetime.now().isoformat(),
            "action": "card_swipe",
            "card_id": payload["card_id"],
            "location_id": payload["location_id"],
            "event_time": payload["timestamp"],
            "status": status
        }

        try:
            requests.post(LOG_URL, json=log_event)
        except requests.exceptions.RequestException as e:
            print(f"WARNING: Could not send log to Logstash: {e}")

        # Simulate real-time delay
        time.sleep(0.05)

    print("\n--- Simulation Complete ---")


if __name__ == "__main__":
    simulate_real_time_swipes()