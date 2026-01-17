# services/gemini.py

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

CATEGORY_DESC = {
    "FOOD": "Food assistance such as food banks, community kitchens, or free meals.",
    "SHELTER": "Shelters, transitional housing, and safe sleeping resources.",
    "HEALTHCARE": "Clinics, medical centers, dental care, or public hospitals.",
    "MENTAL_HEALTH": "Counseling, therapy, or addiction recovery services.",
    "FINANCIAL": "Financial assistance, credit counseling, or emergency relief.",
    "LEGAL": "Legal aid, immigration support, and document assistance.",
    "EDUCATION": "Job training, literacy programs, and educational support.",
    "COMMUNITY": "Community centers, NGOs, support groups, or charities.",
    "TRANSPORTATION": "Public transit assistance or low-cost ride options."
}

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
        "0-3": "Do not instruct the child to travel or call anyone.",
        "4-9": "Do not tell the child to travel alone or contact strangers.",
        "10-12": "Recommend asking a parent before visiting locations.",
        "13-17": "Avoid unsafe travel advice; mention trusted adults.",
        "18+": "No restrictions."
    }.get(age_group, "No restrictions.")

    if places:
        place_text = "\n".join([f"- {p['name']} ({p['distance_km']} km)" for p in places])
    else:
        place_text = "No relevant assistance resources found nearby."

    prompt = f"""
USER CONTEXT:
{conversation}

CATEGORY: {service_type}
CATEGORY_DESCRIPTION: {CATEGORY_DESC.get(service_type, '')}

AGE_GROUP: {age_group}
TONE: {tone}
SAFETY: {safety}

LOCATION:
{location_info.get('formatted')}

NEARBY SUPPORT RESOURCES:
{place_text}

GUIDELINES:
- Be practical and supportive
- Assume user may be in need
- Prioritize free or NGO services first
- Do not hallucinate services
- If no services available, suggest calling local helplines or community NGOs
"""

    res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return res.text.strip()
