def classify_service_type(message: str) -> str:
    """Enhanced intent classification with better keyword matching"""
    message = message.lower()

    # Priority-ordered keywords (more specific first)
    KEYWORDS = {
        "MENTAL_HEALTH": [
            "mental health", "therapy", "therapist", "stress", "anxiety", "depression",
            "counseling", "counselor", "addiction", "rehab", "suicide", "crisis",
            "psychological", "psychiatric", "ptsd", "trauma", "emotional support"
        ],
        "SHELTER": [
            "shelter", "homeless", "place to stay", "need bed", "housing",
            "night shelter", "sleep tonight", "roof", "emergency housing",
            "domestic violence", "safe house", "transitional housing"
        ],
        "MEDICAL": [  # Changed from HEALTHCARE to match places.py
            "hospital", "doctor", "clinic", "medicine", "health", "medical",
            "injury", "sick", "ill", "pain", "emergency room", "urgent care",
            "dentist", "dental", "pharmacy", "prescription", "treatment"
        ],
        "FOOD": [
            "food", "hungry", "meal", "eat", "grocery", "ration",
            "pantry", "food bank", "soup kitchen", "starving", "feed",
            "breakfast", "lunch", "dinner", "nutrition"
        ],
        "LEGAL": [
            "lawyer", "legal aid", "attorney", "court", "advocate", "immigration",
            "documents", "paperwork", "visa", "asylum", "legal help",
            "eviction", "custody", "rights"
        ],
        "FINANCIAL": [
            "money", "loan", "finance", "bills", "credit", "debt",
            "emergency funds", "financial aid", "cash assistance",
            "rent help", "utility assistance", "broke", "poor"
        ],
        "EDUCATION": [
            "school", "college", "study", "education", "learn",
            "training", "courses", "skills", "literacy", "ged",
            "vocational", "job training", "certificate"
        ],
        "TRANSPORTATION": [
            "bus", "train", "taxi", "transport", "ride", "mobility",
            "metro", "subway", "transit", "get to", "travel"
        ],
        "COMMUNITY_NGOS": [  # Changed from COMMUNITY to match places.py
            "ngo", "community center", "charity", "support group",
            "youth center", "senior center", "community service",
            "nonprofit", "volunteer", "outreach"
        ],
        "EMERGENCY": [
            "emergency", "urgent", "crisis", "911", "immediate help",
            "danger", "threat", "abuse", "violence", "life threatening"
        ]
    }

    # Check each category in priority order
    for category, keywords in KEYWORDS.items():
        if any(keyword in message for keyword in keywords):
            return category

    # Default fallback
    return "FOOD"