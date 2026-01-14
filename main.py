from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import ChatRequest, ChatResponse, DiscoverRequest, DiscoverResponse
from services.intent import classify_service_type
from services.geocode import reverse_geocode
from services.places import find_places
from services.gemini import generate_reply

app = FastAPI(title="ConnectCare AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    try:
        service_type = classify_service_type(payload.message)

        location_info = reverse_geocode(payload.latitude, payload.longitude)

        places = find_places(
            latitude=payload.latitude,
            longitude=payload.longitude,
            category=service_type
        )

        reply = generate_reply(
            user_message=payload.message,
            location_info=location_info,
            places=places
        )

        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/discover", response_model=DiscoverResponse)
async def discover(payload: DiscoverRequest):
    try:
        places = find_places(
            latitude=payload.latitude,
            longitude=payload.longitude,
            category=payload.category
        )

        return DiscoverResponse(places=places)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
