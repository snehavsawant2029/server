# services/places.py

import os, math, asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

CATEGORY_MAP = {
    "FOOD": ["grocery_or_supermarket", "supermarket"],
    "SHELTER": ["lodging"],
    "MEDICAL": ["hospital", "doctor", "clinic", "pharmacy"],
    "MENTAL_HEALTH": ["psychologist", "health"],
    "COMMUNITY_NGOS": ["community_center"],
    "FINANCIAL": ["bank", "atm"],
    "LEGAL": ["lawyer", "courthouse"],
    "TRANSPORTATION": ["bus_station", "train_station"],
    "EMERGENCY": ["hospital", "police", "fire_station"],
}

NEEDY_FALLBACK = {
    "FOOD": ["food bank", "food pantry", "free food", "community kitchen"],
    "SHELTER": ["homeless shelter", "night shelter"],
    "MEDICAL": ["free clinic", "public health clinic"],
}

BAD_KEYWORDS = ["atm", "studio", "export", "office", "toilet"]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(d_lon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

async def fetch_json(client, url):
    try:
        r = await client.get(url)
        return r.json()
    except:
        return {}

async def fetch_details(client, pid):
    url = (
        f"https://maps.googleapis.com/maps/api/place/details/json?"
        f"place_id={pid}&fields=formatted_phone_number,rating,user_ratings_total,opening_hours,geometry&key={GOOGLE_API_KEY}"
    )
    return (await fetch_json(client, url)).get("result", {})

async def find_places(lat, lon, category):
    results = {}
    types = CATEGORY_MAP.get(category, [])
    fallbacks = NEEDY_FALLBACK.get(category, [])

    queries = [{"type": t, "keyword": None} for t in types] + \
              [{"type": None, "keyword": kw} for kw in fallbacks]

    # Add a very soft fallback so results never empty
    if category == "FOOD":
        queries.append({"type": None, "keyword": "restaurant"})

    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    async with httpx.AsyncClient(timeout=6.0) as client:
        tasks = []
        for q in queries:
            url = (
                f"{base}?location={lat},{lon}&radius=6000&key={GOOGLE_API_KEY}"
            )
            if q["type"]:
                url += f"&type={q['type']}"
            if q["keyword"]:
                url += f"&keyword={q['keyword']}"
            tasks.append(fetch_json(client, url))

        responses = await asyncio.gather(*tasks)

        for data in responses:
            for p in data.get("results", []):
                name = p.get("name", "").lower()
                if any(b in name for b in BAD_KEYWORDS):
                    continue

                pid = p["place_id"]
                if pid not in results:
                    details = await fetch_details(client, pid)
                    loc = details.get("geometry", {}).get("location", {})
                    dist = haversine(lat, lon, loc.get("lat", lat), loc.get("lng", lon))

                    results[pid] = {
                        "name": p.get("name"),
                        "address": p.get("vicinity"),
                        "distance_km": round(dist, 2),
                        "rating": details.get("rating"),
                        "reviews": details.get("user_ratings_total"),
                        "phone": details.get("formatted_phone_number"),
                        "open_now": p.get("opening_hours", {}).get("open_now") if p.get("opening_hours") else None,
                        "maps_url": f"https://www.google.com/maps/dir/?api=1&destination={loc.get('lat')},{loc.get('lng')}"
                    }

    return sorted(results.values(), key=lambda x: x["distance_km"])[:10]
