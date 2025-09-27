"""
Contains the business logic of the application.
This file handles the storage and retrieval of data, keeping the API
endpoints in main.py clean and focused on handling HTTP requests.
For this prototype, our "database" is a simple Python dictionary.
"""

from schemas.card_swipes import SwipeEvent
from typing import List, Dict

# In-memory database:
# A dictionary where keys are 'card_id's (str) and values are lists
# of SwipeEvent objects for that entity.
entity_timeline_db: Dict[str, List[SwipeEvent]] = {}


def store_swipe(swipe: SwipeEvent) -> SwipeEvent:
    """
    Stores a new swipe event in our in-memory database.

    Args:
        swipe (SwipeEvent): The swipe event data, validated by Pydantic.

    Returns:
        SwipeEvent: The swipe event that was just stored.
    """
    # Use setdefault to create a new list for the card_id if it doesn't exist,
    # then append the new swipe event to that list.
    entity_timeline_db.setdefault(swipe.card_id, []).append(swipe)

    print(
        f"Stored swipe for {swipe.card_id} at {swipe.location_id}. Total swipes for entity: {len(entity_timeline_db[swipe.card_id])}")

    return swipe


def get_timeline(card_id: str) -> List[SwipeEvent]:
    """
    Retrieves the complete timeline for a given card_id.

    Args:
        card_id (str): The ID of the entity whose timeline is requested.

    Returns:
        List[SwipeEvent]: A list of all swipe events for the entity,
                          sorted chronologically by timestamp.
                          Returns an empty list if the card_id is not found.
    """
    # Retrieve the list of swipes for the card_id. If not found, return an empty list.
    swipes = entity_timeline_db.get(card_id, [])

    # Sort the swipes by timestamp in ascending order before returning.
    # The `key=lambda event: event.timestamp` tells the sort function to use
    # the 'timestamp' attribute of each SwipeEvent object for comparison.
    return sorted(swipes, key=lambda event: event.timestamp)
