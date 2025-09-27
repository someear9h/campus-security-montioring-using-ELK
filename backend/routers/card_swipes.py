from fastapi import APIRouter
from typing import List, Dict
from schemas.card_swipes import SwipeEvent

router = APIRouter()

# In-memory database
entity_timeline_db: Dict[str, List[SwipeEvent]] = {}


def store_swipe(swipe: SwipeEvent) -> SwipeEvent:
    entity_timeline_db.setdefault(swipe.card_id, []).append(swipe)
    print(
        f"Stored swipe for {swipe.card_id} at {swipe.location_id}. Total swipes for entity: {len(entity_timeline_db[swipe.card_id])}"
    )
    return swipe


def get_timeline(card_id: str) -> List[SwipeEvent]:
    swipes = entity_timeline_db.get(card_id, [])
    return sorted(swipes, key=lambda event: event.timestamp)


@router.post("/ingest", tags=["Card Swipes"])
def ingest_swipe(swipe: SwipeEvent):
    """
    Endpoint to ingest a new swipe event.
    """
    return store_swipe(swipe)


@router.get("/timeline/{card_id}", tags=["Card Swipes"])
def timeline(card_id: str):
    """
    Endpoint to retrieve the timeline of a card_id.
    """
    return get_timeline(card_id)
