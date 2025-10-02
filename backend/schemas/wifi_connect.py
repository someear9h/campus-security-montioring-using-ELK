from pydantic import BaseModel
from datetime import datetime

class WifiConnectEvent(BaseModel):
    device_hash: str
    ap_id: str
    timestamp: datetime