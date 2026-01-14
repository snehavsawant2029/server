import requests, os
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def reverse_geocode(lat, lon):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    r = requests.get(url)
    data = r.json()

    components = data["results"][0]["address_components"]

    def get(t):
        for c in components:
            if t in c["types"]:
                return c["long_name"]
        return None

    return {
        "city": get("locality"),
        "state": get("administrative_area_level_1"),
        "country": get("country")
    }
