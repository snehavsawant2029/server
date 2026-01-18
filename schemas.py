from pydantic import BaseModel, EmailStr
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str   # "user" or "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    latitude: float
    longitude: float
    age_group: str   # "0-3", "4-9", "10-12", "13-17", "18+"

class ChatResponse(BaseModel):
    reply: str

class DiscoverRequest(BaseModel):
    category: str
    latitude: float
    longitude: float

class Place(BaseModel):
    name: str
    address: str
    distance_miles: float
    phone: Optional[str] = None
    rating: Optional[float] = None
    reviews: Optional[int] = None
    open_now: Optional[bool] = None
    maps_url: Optional[str] = None   # NEW — for Google Maps directions

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str

class DiscoverResponse(BaseModel):
    places: List[Place]
