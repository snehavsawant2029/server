import httpx
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

async def reverse_geocode_async(lat, lon):
    """Async version for better performance"""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            response = await client.get(url)
            data = response.json()
        except:
            return {"formatted": f"Location: {lat}, {lon}"}

    if not data.get("results"):
        return {"formatted": f"Location: {lat}, {lon}"}

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

# Synchronous version for backward compatibility
def reverse_geocode(lat, lon):
    """Synchronous version - consider migrating to async"""
    import requests
    url = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={GOOGLE_API_KEY}"
    
    try:
        data = requests.get(url, timeout=5).json()
    except:
        return {"formatted": f"Location: {lat}, {lon}"}

    if not data.get("results"):
        return {"formatted": f"Location: {lat}, {lon}"}

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