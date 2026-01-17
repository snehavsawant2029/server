def classify_service_type(message: str) -> str:
    message = message.lower()

    KEYWORDS = {
        "FOOD": [
            "food", "hungry", "meal", "grocery", "ration",
            "pantry", "food bank", "kitchen"
        ],
        "SHELTER": [
            "shelter", "homeless", "stay", "bed", "housing",
            "night shelter", "sleep"
        ],
        "HEALTHCARE": [
            "hospital", "doctor", "clinic", "medicine", "health",
            "injury", "medical", "dentist"
        ],
        "MENTAL_HEALTH": [
            "mental", "therapy", "stress", "anxiety", "depression",
            "counseling", "addiction", "rehab"
        ],
        "FINANCIAL": [
            "money", "loan", "finance", "bills", "credit",
            "emergency funds", "financial aid"
        ],
        "LEGAL": [
            "lawyer", "legal", "court", "advocate", "immigration",
            "documents", "paperwork"
        ],
        "EDUCATION": [
            "school", "college", "study", "education",
            "training", "courses", "skills", "literacy"
        ],
        "COMMUNITY": [
            "ngo", "community", "charity", "support", "rehab",
            "youth center", "group", "club"
        ],
        "TRANSPORTATION": [
            "bus", "train", "taxi", "transport", "mobility"
        ],
    }

    for category, keys in KEYWORDS.items():
        if any(k in message for k in keys):
            return category

    # default fallback
    return "FOOD"