import os
import re
import httpx
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from dotenv import load_dotenv

from app.schemas import ChatRequest, ChatResponse, PlaceItem
from app.services import osm, llm
from app.utils.rate_limit import limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

load_dotenv()

MAX_RESULTS = int(os.getenv("MAX_RESULTS", 5))
DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "Jakarta, Indonesia")

app = FastAPI(title="Local LLM + OpenStreetMap Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests"})

async def get_http_client():
    headers = {"User-Agent": f"HeyPico-LLM-OSM/1.0 ({os.getenv('OSM_CONTACT','repo-demo@example.com')})"}
    return httpx.AsyncClient(headers=headers)

CITY_RE = re.compile(r"\b(in|di)\s+([a-zA-Z\s]+)$", re.IGNORECASE)

def parse_city(prompt: str):
    m = CITY_RE.search(prompt.strip())
    return m.group(2).strip() if m else None

@app.get("/")
async def root():
    return HTMLResponse("""
    <h3>Local LLM + OpenStreetMap</h3>
    <p>POST /chat {"prompt": "best seafood in Bandung"}</p>
    """)

@app.post("/chat", response_model=ChatResponse)
@limiter.limit("30/minute")
async def chat(request: Request, req: ChatRequest):
    try:
        # Minimal LLM intent check; safe fallback if it fails
        intent_class = await llm.classify(req.prompt)
        if intent_class != "FIND_PLACES" and not any(w in req.prompt.lower() for w in ["eat", "makan", "visit", "places", "restaurant", "cafe"]):
            return ChatResponse(intent="unknown", message="I can help you find places to eat/go/visit. Try: 'seafood in Senayan'.")

        city = parse_city(req.prompt) or DEFAULT_LOCATION
        
        # Create HTTP client for this request
        async with httpx.AsyncClient(headers={"User-Agent": f"HeyPico-LLM-OSM/1.0 ({os.getenv('OSM_CONTACT','repo-demo@example.com')})"}) as client:
            results = await osm.search_places(client, req.prompt, city, MAX_RESULTS)
            
        if not results:
            raise HTTPException(status_code=404, detail="No places found")

        items = [PlaceItem(**r) for r in results]
        msg = f"Here are some places in {city}. Click a result to open it in OpenStreetMap."

        return ChatResponse(intent="find_places", city=city, items=items, message=msg)
    
    except Exception as e:
        # Log the error and return a safe response
        print(f"Error in chat endpoint: {e}")
        return ChatResponse(intent="error", message=f"An error occurred: {str(e)}")