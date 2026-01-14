def classify_service_type(message: str) -> str:
    message = message.lower()
    if "food" in message or "eat" in message or "meal" in message:
        return "FOOD"
    if "shelter" in message or "sleep" in message:
        return "SHELTER"
    return "FOOD"
