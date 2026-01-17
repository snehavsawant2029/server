# services/places.py

import os, math, asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

RADIUS_TIERS = [3000, 8000, 20000]

CATEGORY_MAP = {
    "FOOD": [
        "food_bank",
        "meal_delivery",
        "community_center",
        "supermarket"
    ],
    "MEDICAL": [
        "clinic",
        "doctor",
        "dentist",
        "hospital",
        "pharmacy",
        "psychologist"
    ],
    "SHELTER": [
        "homeless_shelter",
        "lodging",
        "local_government_office"
    ],
    "EDUCATION": [
        "school",
        "university",
        "library"
    ],
    "FINANCIAL": [
        "bank",
        "credit_union",
        "atm"
    ],
    "COMMUNITY_NGOS": [
        "community_center",
        "church",
        "mosque",
        "hindu_temple",
        "synagogue",
        "park"
    ],
    "LEGAL": [
        "lawyer",
        "courthouse",
        "local_government_office",
        "embassy"
    ],
    "MENTAL_HEALTH": [
        "psychologist",
        "drug_rehab",
        "health"
    ],
    "TRANSPORTATION": [
        "bus_station",
        "train_station",
        "taxi_stand"
    ],
    "EMERGENCY": [
        "hospital",
        "police",
        "fire_station"
    ]
}

BAD_KEYWORDS = ["export", "studio", "luxury", "spa"]

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

async def tier_search(client, lat, lon, types, radius):
    tasks = []
    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    for t in types:
        url = f"{base}?location={lat},{lon}&radius={radius}&key={GOOGLE_API_KEY}&type={t}"
        tasks.append(fetch_json(client, url))
    return await asyncio.gather(*tasks)

async def find_places(lat, lon, category):
    results = {}
    types = CATEGORY_MAP.get(category, [])

    async with httpx.AsyncClient(timeout=6.0) as client:
        for radius in RADIUS_TIERS:
            responses = await tier_search(client, lat, lon, types, radius)

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
                            "open_now": details.get("opening_hours", {}).get("open_now") if details.get("opening_hours") else None,
                            "maps_url": f"https://www.google.com/maps/dir/?api=1&destination={loc.get('lat')},{loc.get('lng')}"
                        }

            # stop early if enough results
            if len(results) >= 8:
                break

    return sorted(results.values(), key=lambda x: x["distance_km"])[:10]
