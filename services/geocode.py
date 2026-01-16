# services/geocode.py

import requests, os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def reverse_geocode(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    data = requests.get(url).json()

    if not data.get("results"):
        return {}

    comp = data["results"][0]["address_components"]

    def get(types):
        for c in comp:
            if any(t in c["types"] for t in types):
                return c["long_name"]
        return None

    return {
        "city": get(["locality"]),
        "state": get(["administrative_area_level_1"]),
        "country": get(["country"]),
        "formatted": data["results"][0]["formatted_address"]
    }
