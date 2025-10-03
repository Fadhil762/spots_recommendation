import os
import httpx
from typing import Any, Dict, List, Optional

CONTACT = os.getenv("OSM_CONTACT", "repo-demo@example.com")
UA = f"HeyPico-LLM-OSM/1.0 ({CONTACT})"

NOMINATIM = "https://nominatim.openstreetmap.org"
OVERPASS = "https://overpass-api.de/api/interpreter"

async def geocode_city(client: httpx.AsyncClient, city: str) -> Optional[dict]:
    params = {"q": city, "format": "json", "limit": 1}
    r = await client.get(f"{NOMINATIM}/search", params=params, headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None

# Simple Overpass query by amenity/category keywords near a lat/lon
OVERPASS_TEMPLATE = (
    "[out:json][timeout:25];"
    "(node[amenity~\"{amenity}\"](around:{radius},{lat},{lon});"
    " way[amenity~\"{amenity}\"](around:{radius},{lat},{lon});"
    " rel[amenity~\"{amenity}\"](around:{radius},{lat},{lon}););"
    "out center;"
)

# Map a few common intents to OSM amenity tags
INTENT_TO_AMENITY = {
    "restaurant": "restaurant|fast_food|cafe|food_court",
    "cafe": "cafe",
    "coffee": "cafe",
    "warung": "restaurant|fast_food",
    "bakso": "restaurant",
    "mie": "restaurant",
    "sate": "restaurant",
    "seafood": "restaurant",
    "museum": "museum",
    "park": "park",
    "mall": "marketplace|mall|supermarket",
}

def guess_amenity(prompt: str) -> str:
    p = prompt.lower()
    for k, v in INTENT_TO_AMENITY.items():
        if k in p:
            return v
    # default catch-all for eating
    if any(w in p for w in ["eat", "makan", "restaurant", "kuliner", "food"]):
        return INTENT_TO_AMENITY["restaurant"]
    # places to go
    if any(w in p for w in ["go", "visit", "tempat", "wisata", "attraction"]):
        return "museum|park|tourism"
    return INTENT_TO_AMENITY["restaurant"]

async def search_places(client: httpx.AsyncClient, prompt: str, city: str, max_results: int = 5) -> List[Dict[str, Any]]:
    city_geo = await geocode_city(client, city)
    if not city_geo:
        return []
    lat = float(city_geo["lat"]) ; lon = float(city_geo["lon"])

    amenity_regex = guess_amenity(prompt)
    q = OVERPASS_TEMPLATE.format(amenity=amenity_regex, radius=5000, lat=lat, lon=lon)

    print(f"Overpass query: {q}")  # Debug logging
    r = await client.post(OVERPASS, data={"data": q}, headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded"}, timeout=40)
    r.raise_for_status()
    data = r.json()

    items = []
    for el in data.get("elements", [])[:max_results]:
        tags = el.get("tags", {})
        name = tags.get("name") or "(Unnamed)"
        center = el.get("center") or {"lat": el.get("lat"), "lon": el.get("lon")}
        if not center["lat"] or not center["lon"]:
            continue
        addr = ", ".join(filter(None, [
            tags.get("addr:street"), tags.get("addr:housenumber"), tags.get("addr:city"), tags.get("addr:postcode")
        ])) or tags.get("addr:full", "")
        items.append({
            "name": name,
            "address": addr,
            "lat": center["lat"],
            "lon": center["lon"],
            "osm_id": str(el.get("id")),
            "category": tags.get("amenity") or tags.get("tourism"),
            "rating": None,
        })
    return items