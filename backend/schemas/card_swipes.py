from pydantic import BaseModel
from datetime import datetime

"""
Defines the Pydantic models for data validation.
Pydantic enforces type hints at runtime, providing robust data validation
and serialization. This file acts as the single source of truth for the
shape of our data.
"""

class SwipeEvent(BaseModel):
    """
    Represents a single card swipe event.

    This model is used to validate the data sent to the /ingest endpoint
    and is also the structure for data returned by the /timeline endpoint.
    """
    card_id: str
    location_id: str
    timestamp: datetime