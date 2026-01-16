# services/gemini.py

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(messages, location_info, places, age_group, service_type):
    conversation = "\n".join([f"{m.role.upper()}: {m.content}" for m in messages])

    tone = {
        "0-3": "Use extremely simple words. Address a parent.",
        "4-9": "Use simple words. Encourage parent involvement.",
        "10-12": "Explain clearly. Suggest asking a trusted adult.",
        "13-17": "Respect autonomy. Avoid risky instructions.",
        "18+": "Normal adult language."
    }.get(age_group, "Normal adult language.")

    safety = {
        "0-3": "Do not instruct child to go anywhere or call anyone.",
        "4-9": "Do not tell child to travel alone or contact strangers.",
        "10-12": "Recommend asking a parent before visiting.",
        "13-17": "Avoid unsafe travel. Mention trusted adults.",
        "18+": "No restrictions."
    }.get(age_group, "No restrictions.")

    fallback = {
        "FOOD": "If nearby food is not listed, try asking for food banks, food pantries, community kitchens, or charity meals.",
        "SHELTER": "If shelters are not listed, ask local NGOs or municipal shelters.",
        "MEDICAL": "If clinics are not listed, try free clinics, public health centers, or government clinics.",
    }.get(service_type, "You may ask local community support groups for help.")

    if places:
        place_text = "\n".join([f"- {p['name']} ({p['distance_km']} km)" for p in places])
    else:
        place_text = f"No matching services found nearby.\n{fallback}"

    prompt = f"""
CONTEXT:
{conversation}

AGE GROUP: {age_group}
TONE: {tone}
SAFETY RULES: {safety}

LOCATION:
{location_info.get('city')}, {location_info.get('state')}, {location_info.get('country')}

SERVICES:
{place_text}

INSTRUCTIONS:
- Be helpful and supportive
- Assume user may be in need
- Do not hallucinate services
- If no services, guide safely and offer options
- Keep simple and practical
"""

    res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return res.text.strip()
