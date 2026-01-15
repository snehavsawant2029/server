import requests, os, math
from dotenv import load_dotenv
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CATEGORY_MAP = {
    "FOOD": {
        "types": ["grocery_or_supermarket", "supermarket", "store", "meal_takeaway"],
        "keywords": ["grocery", "kirana", "provision", "food", "mart"]
    },
    "SHELTER": {
        "types": ["lodging"],
        "keywords": ["hostel", "shelter", "night stay"]
    },
    "MEDICAL": {
        "types": ["hospital", "doctor", "pharmacy", "clinic"],
        "keywords": ["clinic", "medical", "hospital"]
    },
    "MENTAL_HEALTH": {
        "types": ["psychologist", "health"],
        "keywords": ["counseling", "mental", "therapy"]
    },
    "COMMUNITY_NGOS": {
        "types": ["community_center"],
        "keywords": ["ngo", "community", "charity"]
    },
    "FINANCIAL": {
        "types": ["bank", "atm"],
        "keywords": ["bank", "finance"]
    },
    "LEGAL": {
        "types": ["lawyer", "courthouse"],
        "keywords": ["legal", "lawyer", "advocate"]
    },
    "TRANSPORTATION": {
        "types": ["bus_station", "train_station", "taxi_stand"],
        "keywords": ["bus", "taxi", "train"]
    },
    "EMERGENCY": {
        "types": ["hospital", "police", "fire_station"],
        "keywords": ["emergency", "help"]
    }
}

BAD_KEYWORDS = [
    "bank", "atm", "toilet", "studio", "export", "office", "gas", "government"
]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(d_lon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def fetch_details(pid):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={pid}&fields=formatted_phone_number,rating,user_ratings_total,opening_hours,geometry&key={GOOGLE_API_KEY}"
    return requests.get(url).json().get("result", {})

def find_places(lat, lon, category):
    config = CATEGORY_MAP.get(category, None)
    if not config:
        return []

    results = {}
    for t in config["types"]:
        for kw in config["keywords"]:
            url = (
                f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
                f"location={lat},{lon}&radius=6000&type={t}&keyword={kw}&key={GOOGLE_API_KEY}"
            )
            data = requests.get(url).json()

            for p in data.get("results", []):
                name = p.get("name", "").lower()

                if any(b in name for b in BAD_KEYWORDS):
                    continue

                pid = p["place_id"]
                if pid not in results:
                    details = fetch_details(pid)
                    end = details.get("geometry", {}).get("location", {})
                    dist = haversine(lat, lon, end.get("lat", lat), end.get("lng", lon))

                    results[pid] = {
                        "name": p.get("name"),
                        "address": p.get("vicinity"),
                        "distance_km": round(dist, 2),
                        "rating": details.get("rating"),
                        "reviews": details.get("user_ratings_total"),
                        "phone": details.get("formatted_phone_number"),
                        "open_now": p.get("opening_hours", {}).get("open_now") if p.get("opening_hours") else None,
                        "maps_url": f"https://www.google.com/maps/dir/?api=1&destination={end.get('lat')},{end.get('lng')}"
                    }

    cleaned = sorted(results.values(), key=lambda x: x["distance_km"])
    return cleaned[:10]
