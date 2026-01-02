from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(message: str, latitude: float, longitude: float) -> str:
    prompt = f"""
    You are an AI assistant helping users find nearby services.

    User location:
    Latitude: {latitude}
    Longitude: {longitude}
    
    User query:
    {message}

    Give a clear, helpful, and friendly response. If relevant, 
    suggest food, shelter, medical, or community services. 
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    return response.text.strip()

