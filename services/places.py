import os, math, asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Optimized: Start with smaller radius, only expand if needed
RADIUS_TIERS = [5000, 15000]

# Optimized: Reduced keywords to most effective ones
CATEGORY_CONFIG = {
    "FOOD": {
        "keywords": ["food bank", "food pantry", "soup kitchen"],
        "types": [],
        "required_terms": ["food bank", "pantry", "soup kitchen", "food rescue", "meals", "community"]
    },
    "MEDICAL": {
        "keywords": ["free clinic", "community health center", "public health clinic"],
        "types": ["hospital", "pharmacy"],
        "required_terms": ["free clinic", "public hospital"]
    },
    "SHELTER": {
        "keywords": ["homeless shelter", "emergency shelter", "family shelter"],
        "types": [],
        "required_terms": ["homeless shelter", "housing", "mission", "refuge", "haven"]
    },
    "EDUCATION": {
        "keywords": ["public library", "community college", "adult education"],
        "types": ["library"],
        "required_terms": ["library", "school", "education", "college", "university", "learning", "training"]
    },
    "FINANCIAL": {
        "keywords": ["credit union", "community bank"],
        "types": ["bank", "atm"],
        "required_terms": ["bank", "credit union", "financial", "atm"]
    },
    "COMMUNITY_NGOS": {
        "keywords": ["community center", "nonprofit organization", "ymca"],
        "types": ["community_center"],
        "required_terms": ["community", "center", "service", "nonprofit", "organization", "ymca", "ywca", "mission"]
    },
    "LEGAL": {
        "keywords": ["legal aid", "free legal services", "legal clinic"],
        "types": [],
        "required_terms": ["legal aid", "legal services", "legal clinic", "legal assistance", "pro bono", "public defender"]
    },
    "MENTAL_HEALTH": {
        "keywords": ["mental health clinic", "counseling center", "crisis center"],
        "types": ["health"],
        "required_terms": ["mental health", "counseling", "therapy", "psychiatric", "behavioral health", "crisis", "support", "rehab", "treatment"]
    },
    "TRANSPORTATION": {
        "keywords": ["bus station", "train station", "subway station"],
        "types": ["transit_station"],
        "required_terms": ["bus", "train", "transit", "station", "metro", "subway", "rail"]
    },
    "EMERGENCY": {
        "keywords": ["emergency room", "urgent care", "police station"],
        "types": ["hospital", "police", "fire_station"],
        "required_terms": ["emergency", "hospital", "urgent care", "police", "fire station", "crisis"]
    }
}

BAD_KEYWORDS = [
    "attorney", "lawyer", "law firm", "legal services", "attorneys at law",
    "injury lawyer", "accident attorney", "esq", "law offices",
    "luxury", "spa", "resort", "hotel", "premium", "boutique",
    "at&t", "verizon", "t-mobile", "sprint", "wireless",
    "restaurant", "cafe", "coffee", "bar", "pub", "grill", "bistro",
    "pizzeria", "diner", "eatery", "bakery", "catering",
    "real estate", "property management", "realty"
]

CATEGORY_EXCEPTIONS = {
    "FOOD": ["market", "grocery", "supermarket"],
    "FINANCIAL": ["store"],
    "LEGAL": ["attorney", "lawyer", "law", "legal"]
}

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2-lat1)
    d_lon = math.radians(lon2-lon1)
    a = math.sin(d_lat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(d_lon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

async def fetch_json(client, url):
    try:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()
    except:
        return {}

async def fetch_details_batch(client, place_ids):
    """Fetch details for multiple places in parallel"""
    tasks = []
    for pid in place_ids:
        url = (
            f"https://maps.googleapis.com/maps/api/place/details/json?"
            f"place_id={pid}&fields=formatted_phone_number,rating,user_ratings_total,opening_hours,geometry&key={GOOGLE_API_KEY}"
        )
        tasks.append(fetch_json(client, url))
    
    responses = await asyncio.gather(*tasks)
    return {place_ids[i]: resp.get("result", {}) for i, resp in enumerate(responses)}

async def text_search(client, query, lat, lon, radius):
    base = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    url = f"{base}?query={query}&location={lat},{lon}&radius={radius}&key={GOOGLE_API_KEY}"
    return await fetch_json(client, url)

async def nearby_search(client, lat, lon, place_type, radius):
    base = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    url = f"{base}?location={lat},{lon}&radius={radius}&type={place_type}&key={GOOGLE_API_KEY}"
    return await fetch_json(client, url)

def quick_filter(name, types, category, config):
    """Fast initial filter before detailed checks"""
    name_lower = name.lower()
    
    # Quick bad keyword check
    exceptions = CATEGORY_EXCEPTIONS.get(category, [])
    for bad in BAD_KEYWORDS:
        if bad not in exceptions and bad in name_lower:
            return False
    
    # Quick required term check
    required_terms = config.get("required_terms", [])
    if required_terms:
        if not any(term in name_lower for term in required_terms):
            return False
    
    return True

def is_relevant_result(place, category, config):
    """Detailed filtering for remaining candidates"""
    name = place.get("name", "").lower()
    types = place.get("types", [])
    
    if category == "FOOD":
        good_indicators = ["food bank", "pantry", "soup kitchen", "food rescue", 
                          "salvation army", "church", "mission", "community", "free food",
                          "meals", "feeding", "hunger"]
        bad_types = ["restaurant", "cafe", "bar", "meal_delivery", "meal_takeaway", 
                    "bakery", "grocery_or_supermarket", "store"]
        
        if any(t in types for t in bad_types):
            if not any(indicator in name for indicator in good_indicators):
                return False
        
        return any(indicator in name for indicator in good_indicators)
    
    elif category == "MEDICAL":
        bad_medical = ["attorney", "lawyer", "law offices", "legal", "injury law"]
        return not any(bad in name for bad in bad_medical)
    
    elif category == "SHELTER":
        shelter_terms = ["shelter", "housing", "homeless", "mission", "refuge", "safe house", "haven"]
        return any(term in name for term in shelter_terms)
    
    elif category == "LEGAL":
        legal_aid_terms = ["legal aid", "legal services", "pro bono", "legal clinic", 
                          "public defender", "legal assistance", "community legal"]
        private_law = ["injury", "accident", "personal injury", "law firm", "attorneys at law"]
        
        if any(term in name for term in private_law):
            return False
        
        return any(term in name for term in legal_aid_terms)
    
    elif category == "MENTAL_HEALTH":
        mh_terms = ["mental health", "counseling", "therapy", "psychiatric", "behavioral", 
                   "crisis", "support", "rehab", "treatment", "wellness"]
        return any(term in name for term in mh_terms)
    
    elif category == "TRANSPORTATION":
        transit_terms = ["station", "terminal", "stop", "depot", "transit"]
        return any(term in name for term in transit_terms)
    
    elif category == "EMERGENCY":
        emergency_terms = ["emergency", "hospital", "police", "fire", "911", "crisis", "urgent care"]
        return any(term in name for term in emergency_terms)
    
    return True

async def find_places(lat, lon, category):
    results = {}
    config = CATEGORY_CONFIG.get(category, {"keywords": [], "types": [], "required_terms": []})
    
    # Use connection pooling for better performance
    limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)
    async with httpx.AsyncClient(timeout=8.0, limits=limits) as client:
        
        for radius in RADIUS_TIERS:
            # Build all search tasks
            tasks = []
            
            # Text searches (prioritized)
            for keyword in config["keywords"]:
                tasks.append(text_search(client, keyword, lat, lon, radius))
            
            # Type searches (supplement)
            for place_type in config["types"]:
                tasks.append(nearby_search(client, lat, lon, place_type, radius))
            
            # Execute all searches in parallel
            responses = await asyncio.gather(*tasks)
            
            # Quick filtering pass
            candidates = {}
            for data in responses:
                for p in data.get("results", []):
                    pid = p["place_id"]
                    if pid in results or pid in candidates:
                        continue
                    
                    # Fast initial filter
                    if quick_filter(p.get("name", ""), p.get("types", []), category, config):
                        candidates[pid] = p
            
            # Detailed filtering
            filtered_candidates = {}
            for pid, p in candidates.items():
                if is_relevant_result(p, category, config):
                    filtered_candidates[pid] = p
            
            # Batch fetch details for filtered candidates
            if filtered_candidates:
                place_ids = list(filtered_candidates.keys())
                details_map = await fetch_details_batch(client, place_ids)
                
                for pid, p in filtered_candidates.items():
                    details = details_map.get(pid, {})
                    loc = details.get("geometry", {}).get("location", p.get("geometry", {}).get("location", {}))
                    
                    if not loc:
                        continue
                    
                    dist = haversine(lat, lon, loc.get("lat", lat), loc.get("lng", lon))
                    dist_miles = dist*0.621371
                    
                    results[pid] = {
                        "name": p.get("name"),
                        "address": p.get("formatted_address", p.get("vicinity")),
                        "distance_miles": round(dist_miles, 2),
                        "rating": details.get("rating"),
                        "reviews": details.get("user_ratings_total"),
                        "phone": details.get("formatted_phone_number"),
                        "open_now": details.get("opening_hours", {}).get("open_now") if details.get("opening_hours") else None,
                        "maps_url": f"https://www.google.com/maps/dir/?api=1&destination={loc.get('lat')},{loc.get('lng')}&destination_place_id={pid}"
                    }
            
            # Early exit if we have enough results
            if len(results) >= 10:
                break
        
        # Sort by distance
        sorted_results = sorted(results.values(), key=lambda x: x["distance_miles"])
        
        # Priority sorting for specific categories
        if category in ["FOOD", "SHELTER", "LEGAL", "MENTAL_HEALTH"]:
            priority_terms = config.get("required_terms", [])[:3]
            priority = []
            regular = []
            
            for place in sorted_results:
                name_lower = place["name"].lower()
                if any(term in name_lower for term in priority_terms):
                    priority.append(place)
                else:
                    regular.append(place)
            
            sorted_results = priority + regular
        
        return sorted_results[:10]