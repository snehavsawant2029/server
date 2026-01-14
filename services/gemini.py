from google import genai
from dotenv import load_dotenv
import os
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(user_message, location_info, places):
    place_text = "\n".join([f"- {p['name']} ({p['distance_km']} km)" for p in places]) or "No services nearby"

    prompt = f"""
User asked: {user_message}

Location: {location_info}

Nearby relevant services:
{place_text}

Respond politely and helpful only about finding relevant local services. Do not talk about anything else.
"""
    res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return res.text.strip()
