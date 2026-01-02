from pydantic import BaseModel
class ChatRequest(BaseModel):
    message: str
    latitude: float
    longitude: float

class ChatResponse(BaseModel):
    reply: str