import pandas as pd
import requests
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = "data/campus_card_swipes.csv"

# The full URL of the API endpoint that will receive the data.
API_URL = "http://127.0.0.1:8000/card-swipes/ingest"


def simulate_real_time_swipes():
    """
    Reads historical swipe data from a CSV, sorts it by time, and sends it
    to the FastAPI server one-by-one to simulate a live feed of events.
    """
    print("--- Starting Real-Time Data Simulation ---")

    # We use a try...except block to handle potential errors gracefully,
    # like the CSV file not being found.
    try:
        # STEP 1: LOAD THE HISTORICAL DATA
        # We use the pandas library to easily read the CSV into a DataFrame.
        df = pd.read_csv(CSV_PATH)
        print(f"Successfully loaded {len(df)} records from '{CSV_PATH}'.")

        # The 'timestamp' column is just text right now. We convert it into
        # a real datetime object so we can sort it accurately.
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    except FileNotFoundError:
        print(f"FATAL ERROR: The file was not found at '{CSV_PATH}'.")
        print("Please ensure the path is correct and you are running the script from the project's root directory.")
        return # Stop the script if the file doesn't exist.

    # STEP 2: ORDER THE EVENTS CHRONOLOGICALLY
    # This is the most critical step for a realistic simulation. In the real world,
    # events happen in a specific order. We must process our historical data
    # in that same order.
    df.sort_values(by='timestamp', inplace=True)
    print("All swipe records have been sorted by timestamp to ensure chronological processing.")

    # STEP 3: "REPLAY" EACH EVENT ONE-BY-ONE
    # We loop through every single row in our sorted DataFrame.
    print("\n--- Sending swipe data to the server... ---")
    for index, row in df.iterrows():

        # Prepare the data for sending. We convert the pandas row into a
        # Python dictionary, which will then be converted to JSON.
        # The .isoformat() is crucial because it formats the datetime into a
        # standard string (like "2025-09-04T04:29:08") that our Pydantic
        # model on the server expects.
        payload = {
            "card_id": row['card_id'],
            "location_id": row['location_id'],
            "timestamp": row['timestamp'].isoformat()
        }

        try:
            # STEP 4: SEND THE DATA TO THE API
            # This is where the script communicates with our FastAPI server.
            # We make a POST request to the API_URL, sending our `payload`.
            response = requests.post(API_URL, json=payload)

            # A status code of 201 means "Created", which is what our API
            # sends back on success. We check for this to confirm it worked.
            if response.status_code in [200, 201]:
                print(f"SUCCESS: Sent {payload['card_id']} -> {payload['location_id']}")
            else:
                # If something went wrong on the server, we print the error.
                print(f"FAILURE: Server returned status {response.status_code}. Response: {response.text}")

        except requests.exceptions.ConnectionError:
            print(f"\nFATAL ERROR: Could not connect to the server at {API_URL}.")
            print("Please make sure your FastAPI server is running before executing this script.")
            return # Stop the simulation if the server isn't available.

        # STEP 5: SIMULATE THE PASSAGE OF TIME
        # We pause the script for a very short time. This prevents all 10,000+
        # records from being sent in a single second. It "drip-feeds" the data,
        # making it feel like a genuine, real-time stream of events.
        time.sleep(0.05) # Pause for 50 milliseconds

    print("\n--- Simulation Complete: All records have been sent. ---")


# This standard Python construct ensures that the simulation function
# is called only when you run this file directly.
if __name__ == "__main__":
    simulate_real_time_swipes()

