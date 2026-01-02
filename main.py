from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    reply = generate_reply(
        message=payload.message,
        latitude=payload.latitude,
        longitude=payload.longitude
    )
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=f"Chat generation failed: {str(e)}"
    )



