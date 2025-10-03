from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=2, max_length=500)
    
class PlaceItem(BaseModel):
    name : str
    address : str
    lat : float
    lon: float
    osm_id: str
    category: str | None = None
    rating: float | None = None

class ChatResponse(BaseModel):
    intent: str
    city: Optional[str] = None
    items: List[PlaceItem] = []
    message: str