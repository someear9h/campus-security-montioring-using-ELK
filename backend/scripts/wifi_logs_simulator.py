import pandas as pd
import requests
import time
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
CSV_PATH = PROJECT_ROOT / "data" / "wifi_associations_logs.csv"

API_URL = "http://127.0.0.1:8000/wifi-connect/ingest"
LOG_URL = "http://127.0.0.1:5045"

def simulate_real_time_wifi_logs():
    print("----- starting real time data simulation")

    try:
        df = pd.read_csv(CSV_PATH)
        print(f"Loaded {len(df)} records from '{CSV_PATH}'")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except FileNotFoundError:
        print(f"FATAL ERROR: File not found at '{CSV_PATH}'")
        return

    df.sort_values(by='timestamp', inplace=True)
    print("Wi-Fi logs sorted by timestamp")

    for _, row in df.iterrows():
        payload = {
            "device_hash": row['device_hash'],
            "ap_id": row['ap_id'],
            "timestamp": row['timestamp'].isoformat()
        }

        # Send to FastAPI
        try:
            response = requests.post(API_URL, json=payload)
            status = "success" if response.status_code in [200, 201] else "failed"

            if status == "success":
                print(f"SUCCESS: {payload['device_hash']} -> {payload['ap_id']}")
            else:
                print(f"FAILURE: {response.status_code}, {response.text}")
        except requests.exceptions.ConnectionError:
            print(f"\nFATAL ERROR: Could not connect to {API_URL}. Is FastAPI running?")
            return

        # Send log to Logstash
        headers = {"Content-Type": "application/json"}

        log_event = {
            "event_time": row['timestamp'].isoformat(),
            "action": "wifi-connected",
            "user_id": payload["device_hash"],
            "location": payload["ap_id"]
        }

        try:
            response = requests.post(LOG_URL, json=log_event, headers=headers)
            if response.status_code not in [200, 201]:
                print(f"Logstash log failed: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"WARNING: Could not send log to Logstash: {e}")

        time.sleep(0.05)

    print("\n--- Simulation Complete ---")

if __name__=="__main__":
    simulate_real_time_wifi_logs()
