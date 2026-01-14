import requests, os, math
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CATEGORY_MAP = {
    "FOOD": ["food_bank", "supermarket"],
    "SHELTER": ["lodging"],
    "MEDICAL": ["hospital", "doctor", "pharmacy"],
    "MENTAL_HEALTH": ["psychologist", "health"],
    "COMMUNITY_NGOS": ["local_government_office", "community_center"],
    "RETIREMENT_HOMES": ["nursing_home"],
    "FINANCIAL": ["bank", "atm"],
    "LEGAL": ["courthouse", "lawyer"],
    "EDUCATION": ["school", "university", "library"],
    "TRANSPORTATION": ["bus_station", "taxi_stand"],
    "EMERGENCY": ["police", "fire_station", "hospital"],
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(d_lon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def find_places(latitude, longitude, category):
    types = CATEGORY_MAP.get(category, [])
    results = []

    for t in types:
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={latitude},{longitude}&radius=7000&type={t}&key={GOOGLE_API_KEY}"
        r = requests.get(url).json()

        for p in r.get("results", []):
            dist = haversine(latitude, longitude, p["geometry"]["location"]["lat"], p["geometry"]["location"]["lng"])
            results.append({
                "name": p.get("name"),
                "address": p.get("vicinity"),
                "distance_km": round(dist, 2),
            })

    results.sort(key=lambda x: x["distance_km"])
    return results[:10]
