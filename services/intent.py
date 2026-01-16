# services/intent.py

def classify_service_type(message: str) -> str:
    message = message.lower()

    KEYWORDS = {
        "FOOD": ["food", "eat", "meal", "grocery", "ration", "hungry", "pantry", "food bank"],
        "SHELTER": ["shelter", "sleep", "stay", "bed", "homeless"],
        "MEDICAL": ["hospital", "doctor", "clinic", "medicine", "health", "injury"],
        "MENTAL_HEALTH": ["mental", "counsel", "therapy", "stress", "anxiety", "depression"],
        "FINANCIAL": ["money", "loan", "finance", "bank"],
        "LEGAL": ["lawyer", "legal", "court", "advocate"],
        "EDUCATION": ["school", "college", "study", "education"],
        "COMMUNITY_NGOS": ["ngo", "community", "charity"],
        "RETIREMENT_HOMES": ["old age", "senior", "retire"],
        "TRANSPORTATION": ["bus", "train", "taxi", "transport"],
        "EMERGENCY": ["emergency", "police", "fire", "ambulance"],
    }

    for category, keys in KEYWORDS.items():
        if any(k in message for k in keys):
            return category

    return "FOOD"
