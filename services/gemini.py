# services/gemini.py

from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Updated to match places.py categories
CATEGORY_DESC = {
    "FOOD": "Food assistance including food banks, food pantries, soup kitchens, and free meal programs",
    "MEDICAL": "Free or low-cost medical care including community health clinics, hospitals, pharmacies, and dental services",
    "SHELTER": "Emergency shelters, homeless shelters, transitional housing, and safe sleeping resources",
    "MENTAL_HEALTH": "Mental health services including counseling, therapy, crisis intervention, and addiction recovery programs",
    "FINANCIAL": "Financial assistance programs, emergency funds, bill payment help, and credit counseling",
    "LEGAL": "Free legal aid, legal clinics, pro bono services, immigration help, and document assistance",
    "EDUCATION": "Educational support including libraries, adult education, job training, GED programs, and literacy services",
    "COMMUNITY_NGOS": "Community centers, nonprofit organizations, support groups, faith-based organizations, and charitable services",
    "TRANSPORTATION": "Public transit information, bus/train stations, and transportation assistance programs",
    "EMERGENCY": "Emergency services including hospitals, police, fire departments, crisis centers, and urgent care"
}

def generate_reply(messages, location_info, places, age_group, service_type):
    """Generate AI response with strict app-focused guidelines"""
    
    # Build conversation history
    conversation = "\n".join([f"{m.role.upper()}: {m.content}" for m in messages])

    # Format places list with AGE-APPROPRIATE restrictions
    if places:
        place_list = []
        for i, p in enumerate(places[:5], 1):  # Show top 5
            phone = f"\n   📞 Phone: {p['phone']}" if p.get('phone') else ""
            rating = f" • Rating: {p['rating']}/5" if p.get('rating') else ""
            open_status = ""
            if p.get('open_now') is not None:
                open_status = " • ✓ Open now" if p['open_now'] else " • Closed now"
            
            # Age-based information restriction
            if age_group == "0-3":
                # Only name and basic info - NO address, phone, or directions
                place_list.append(
                    f"**{i}. {p['name']}**{rating}"
                )
            elif age_group == "4-9":
                # Only name and address - NO phone or directions
                place_list.append(
                    f"**{i}. {p['name']}**{rating}{open_status}  \n"
                    f"📍 {p['address']} ({p['distance_miles']} km away)"
                )
            elif age_group == "10-12":
                # Full info including directions, but will ask parent to go with them
                place_list.append(
                    f"**{i}. {p['name']}**{rating}{open_status}  \n"
                    f"📍 {p['address']} ({p['distance_miles']} km away){phone}  \n"
                    f"🗺️ [Get Directions]({p['maps_url']})"
                )
            else:  # 13-17 and 18+
                # Full information
                place_list.append(
                    f"**{i}. {p['name']}**{rating}{open_status}  \n"
                    f"📍 {p['address']} ({p['distance_miles']} km away){phone}  \n"
                    f"🗺️ [Get Directions]({p['maps_url']})"
                )
        
        place_text = "\n\n".join(place_list)
    else:
        place_text = "Unfortunately, no specific resources were found in your immediate area."

    # Simplified, more direct prompt based on age
    if age_group == "0-3":
        prompt = f"""You are helping a PARENT/GUARDIAN seeking {service_type.replace('_', ' ').lower()} for their young child (age 0-3).

CONVERSATION:
{conversation}

LOCATION: {location_info.get('formatted', 'Unknown')}

RESOURCES FOUND:
{place_text}

RESPONSE STRUCTURE (MANDATORY):

1. **Address the Parent** (2-3 sentences):
   "I see you're seeking {service_type.replace('_', ' ').lower()} help for your young child. [Educational context about why this is important for young children]. [What these services provide]."

2. **Present Resources**:
   Show the resources above with this introduction:
   "Here are child-friendly/family-friendly resources near you:"
   [List the resources]

3. **Parent Guidance** (3-4 sentences):
   - "As a parent, I recommend..."
   - Which resource to contact first and why
   - What to ask when calling (availability, age requirements, etc.)
   - What to bring or prepare
   
4. **Closing**:
   "You're taking an important step in supporting your child. Let me know if you need help with anything else."

CRITICAL: NEVER address the child. Only speak to the parent/guardian.

Generate response:"""

    elif age_group == "4-9":
        prompt = f"""You are helping a PARENT/GUARDIAN seeking {service_type.replace('_', ' ').lower()} for their child (age 4-9).

CONVERSATION:
{conversation}

LOCATION: {location_info.get('formatted', 'Unknown')}

RESOURCES FOUND:
{place_text}

RESPONSE STRUCTURE (MANDATORY):

1. **Address the Parent** (2-3 sentences):
   "I understand your child needs help with {service_type.replace('_', ' ').lower()}. [Educational context]. [What these services provide for children this age]."

2. **Present Resources**:
   "Here are family-friendly resources near you:"
   [List the resources]

3. **Parent Guidance** (4-5 sentences):
   - "Please accompany your child to these locations."
   - Which resource to try first and why
   - What to explain to your child in simple terms
   - What documents or information to bring
   - How to prepare your child for the visit

4. **Closing**:
   "Your support means everything to your child. Let me know if you need more help."

Generate response:"""

    elif age_group == "10-12":
        prompt = f"""You are helping a young person (age 10-12) seeking {service_type.replace('_', ' ').lower()}.

CONVERSATION:
{conversation}

LOCATION: {location_info.get('formatted', 'Unknown')}

RESOURCES FOUND:
{place_text}

RESPONSE STRUCTURE (MANDATORY):

1. **Acknowledge with Empathy** (2-3 sentences):
   "I understand you need help with {service_type.replace('_', ' ').lower()}. [Educational context about the issue]. [Why these resources can help]."

2. **Present Resources**:
   "Here are resources near you that can help:"
   [List the resources]

3. **Guidance with Adult Support** (3-4 sentences):
   - Recommend which resource seems best and why
   - "Please talk to a parent, guardian, or trusted adult before visiting"
   - "They can help you call ahead and go with you"
   - What to expect when you get there

4. **Closing**:
   "You're being very responsible by seeking help. A trusted adult can support you through this. Let me know if you have questions."

Generate response:"""

    elif age_group == "13-17":
        prompt = f"""You are helping a teenager (age 13-17) seeking {service_type.replace('_', ' ').lower()}.

CONVERSATION:
{conversation}

LOCATION: {location_info.get('formatted', 'Unknown')}

RESOURCES FOUND:
{place_text}

RESPONSE STRUCTURE (MANDATORY):

1. **Respectful Acknowledgment** (2-3 sentences):
   "I understand you're seeking {service_type.replace('_', ' ').lower()} support. [Educational context]. [What these services offer and how they help teens]."

2. **Present Resources**:
   "Here are resources near you:"
   [List the resources]

3. **Practical Guidance** (3-4 sentences):
   - Recommend best options with reasoning
   - What to ask when calling (confidentiality, parent consent requirements, etc.)
   - "Consider talking to a trusted adult if you're comfortable - they can provide support"
   - What to bring (ID, insurance if applicable)

4. **Closing**:
   "You're taking a brave step by reaching out. You deserve support. Let me know if you need anything else."

IMPORTANT: If this is about mental health crisis, start with: "🆘 If you're in immediate crisis, call 988 Suicide & Crisis Lifeline."

Generate response:"""

    else:  # 18+
        prompt = f"""You are helping an adult seeking {service_type.replace('_', ' ').lower()}.

CONVERSATION:
{conversation}

LOCATION: {location_info.get('formatted', 'Unknown')}

RESOURCES FOUND:
{place_text}

RESPONSE STRUCTURE (MANDATORY):

1. **Direct Acknowledgment** (2-3 sentences):
   "I understand you need {service_type.replace('_', ' ').lower()} support. [Educational context about the service type]. [What to expect from these services]."

2. **Present Resources**:
   "Here are resources near you:"
   [List the resources]

3. **Actionable Steps** (4-5 sentences):
   - "I recommend starting with [specific resource] because [reason]"
   - "Call [phone] to schedule an appointment or ask about walk-in hours"
   - What to prepare: ID, proof of residency, income documents, insurance, etc.
   - "Ask about: [fees/sliding scale, wait times, intake requirements]"
   - Typical timeline (same-day, within a week, etc.)

4. **Closing**:
   "You deserve support. Don't hesitate to reach out. Let me know if you need help with anything else."

Generate response:"""

    try:
        response = client.models.generate_content(
            model="gemini-1.5-pro",  # Most reliable for instruction following
            contents=prompt,
            config={
                "temperature": 0.8,
                "top_p": 0.95,
                "max_output_tokens": 1000,
            }
        )
        
        # Check if response was generated
        if response and response.text:
            return response.text.strip()
        else:
            raise Exception("Empty response from Gemini")
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        print(f"Age group: {age_group}, Service: {service_type}")
        
        # Better age-appropriate fallback
        if age_group in ["0-3", "4-9"]:
            return f"""I see you're seeking {service_type.lower().replace('_', ' ')} help for your child.

{CATEGORY_DESC.get(service_type, 'These services can provide the support your family needs.')}

**Resources near you:**

{place_text if places else 'Unfortunately, no specific resources were found nearby. Please call 211 (United Way) for local assistance referrals.'}

**As a parent, here's what I recommend:**
- Call the closest resource to ask about their services for children
- Ask about age requirements and what documents to bring
- Most services are free or low-cost for families in need

You're taking an important step in supporting your child. Let me know if you need help with anything else."""
        
        elif age_group in ["10-12", "13-17"]:
            return f"""I understand you need {service_type.lower().replace('_', ' ')} support.

{CATEGORY_DESC.get(service_type, 'These services can help you.')}

**Resources near you:**

{place_text if places else 'Unfortunately, no specific resources were found nearby. Please call 211 (United Way) for local assistance referrals.'}

**What to do next:**
- Talk to a parent, guardian, or trusted adult about visiting these resources
- They can help you call ahead and go with you
- Bring any ID or documents if you have them

You're being responsible by seeking help. Let me know if you have questions."""
        
        else:  # 18+
            return f"""I understand you need {service_type.lower().replace('_', ' ')} support.

{CATEGORY_DESC.get(service_type, 'These services can provide assistance.')}

**Resources near you:**

{place_text if places else 'Unfortunately, no specific resources were found nearby. Please call 211 (United Way) for local assistance referrals.'}

**Next steps:**
1. Call the resource that best fits your needs
2. Ask about their intake process and requirements
3. Prepare any necessary documents (ID, proof of residency, etc.)

You deserve support. Let me know if you need help with anything else."""