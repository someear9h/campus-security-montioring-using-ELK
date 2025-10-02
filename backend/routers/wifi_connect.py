from fastapi import APIRouter, HTTPException
from typing import List
from schemas.wifi_connect import WifiConnectEvent
from services import wifi_connect

router = APIRouter()


@router.post("/ingest", response_model=WifiConnectEvent)
def ingest_wifi_log(log: WifiConnectEvent):
    """
    Endpoint to ingest a new Wi-Fi connection event.
    """
    # Calls the corresponding service function to handle the business logic.
    return wifi_connect.store_wifi_log(log)


@router.get("/timeline/{device_hash}", response_model=List[WifiConnectEvent])
def get_device_timeline(device_hash: str):
    """
    Endpoint to retrieve the connection timeline for a specific device hash.
    """
    timeline = wifi_connect.get_wifi_timeline(device_hash)
    if not timeline:
        raise HTTPException(
            status_code=404,
            detail=f"No Wi-Fi activity found for device_hash: {device_hash}"
        )
    return timeline
