"""
Contains the business logic for handling Wi-Fi association logs.
This service uses an in-memory dictionary to store and retrieve
Wi-Fi connection events for a given device.
"""

from schemas.wifi_connect import WifiConnectEvent
from typing import List, Dict

# In-memory database for Wi-Fi logs:
# A dictionary where keys are 'device_hash' (str) and values are lists
# of WifiConnectEvent objects for that device.
wifi_timeline_db: Dict[str, List[WifiConnectEvent]] = {}


def store_wifi_log(log: WifiConnectEvent) -> WifiConnectEvent:
    """
    Stores a new Wi-Fi connection event in our in-memory database.

    Args:
        log (WifiConnectEvent): The Wi-Fi log data, validated by Pydantic.

    Returns:
        WifiConnectEvent: The Wi-Fi log event that was just stored.
    """
    # Use setdefault to create a new list for the device_hash if it doesn't exist,
    # then append the new log event to that list.
    wifi_timeline_db.setdefault(log.device_hash, []).append(log)

    print(
        f"Stored Wi-Fi log for {log.device_hash} at {log.ap_id}. Total logs for device: {len(wifi_timeline_db[log.device_hash])}")

    return log


def get_wifi_timeline(device_hash: str) -> List[WifiConnectEvent]:
    """
    Retrieves the complete connection timeline for a given device_hash.

    Args:
        device_hash (str): The ID of the device whose timeline is requested.

    Returns:
        List[WifiConnectEvent]: A list of all connection events for the device,
                                sorted chronologically by timestamp.
                                Returns an empty list if the device_hash is not found.
    """
    # Retrieve the list of logs for the device_hash. If not found, return an empty list.
    logs = wifi_timeline_db.get(device_hash, [])

    # Sort the logs by timestamp in ascending order before returning.
    return sorted(logs, key=lambda event: event.timestamp)
