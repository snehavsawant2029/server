from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    latitude: float
    longitude: float

class ChatResponse(BaseModel):
    reply: str

class DiscoverRequest(BaseModel):
    category: str
    latitude: float
    longitude: float

class Place(BaseModel):
    name: str
    address: str
    distance_km: float
    phone: Optional[str] = None

class DiscoverResponse(BaseModel):
    places: List[Place]
