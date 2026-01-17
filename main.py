# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatRequest, ChatResponse, DiscoverRequest, DiscoverResponse, ContactRequest
from services.intent import classify_service_type
from services.geocode import reverse_geocode
from services.places import find_places
from services.gemini import generate_reply
from services.email import send_contact_email
import asyncio

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
        latest_message = payload.messages[-1].content
        service_type = classify_service_type(latest_message)

        location_info = reverse_geocode(payload.latitude, payload.longitude)
        places = await find_places(payload.latitude, payload.longitude, service_type)

        reply = generate_reply(
            messages=payload.messages,
            location_info=location_info,
            places=places,
            age_group=payload.age_group,
            service_type=service_type
        )

        return ChatResponse(reply=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/discover", response_model=DiscoverResponse)
async def discover(payload: DiscoverRequest):
    try:
        places = await find_places(payload.latitude, payload.longitude, payload.category)
        return DiscoverResponse(places=places)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact")
async def contact(payload: ContactRequest):
    try:
        send_contact_email(
            name=payload.name,
            email=payload.email,
            subject=payload.subject,
            message=payload.message
        )

        return {"success": True, "message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))