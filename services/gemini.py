from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_reply(messages, location_info, places, age_group):
    conversation = ""
    for m in messages:
        conversation += f"{m.role.upper()}: {m.content}\n"

    tone = {
        "0-3": "Use extremely simple words. Address a parent.",
        "4-9": "Use simple kid-friendly words. Encourage parent help.",
        "10-12": "Explain clearly. Suggest asking a trusted adult.",
        "13-17": "Respect autonomy but avoid risky instructions.",
        "18+": "Normal adult language."
    }.get(age_group, "Normal adult language.")

    safety = {
        "0-3": "Do not instruct child to go anywhere or call anyone.",
        "4-9": "Do not instruct to travel alone or contact strangers.",
        "10-12": "Recommend asking a parent before going or calling.",
        "13-17": "Avoid unsafe self-navigation. Mention trusted adults.",
        "18+": "No restrictions."
    }.get(age_group, "No restrictions.")

    place_text = "\n".join([
        f"- {p['name']} ({p['distance_km']} km)"
        for p in places
    ]) or "No services found."

    prompt = f"""
CONTEXT:
{conversation}

AGE GROUP: {age_group}
TONE STYLE: {tone}
SAFETY RULES: {safety}

LOCATION:
{location_info.get('city')}, {location_info.get('state')}, {location_info.get('country')}

SERVICES:
{place_text}

RESPOND WITH:
- Helpful, age-appropriate guidance
- Follow safety rules
- If no services, suggest safe alternatives
- Do not hallucinate services
"""

    res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return res.text.strip()
