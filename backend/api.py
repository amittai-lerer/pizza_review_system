# --- api.py ---
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from datetime import datetime
from typing import List
from backend.core import get_pizza_answer
from backend.cache import get_cache_stats, get_cached_entries
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# -------------------------------
# 🔐 Security Configuration
# -------------------------------

API_KEY_NAME = "X-Admin-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    """Validate admin API key."""
    if not api_key_header or api_key_header != os.getenv("ADMIN_API_KEY"):
        raise HTTPException(
            status_code=403,
            detail="Could not validate admin credentials"
        )
    return api_key_header

# -------------------------------
# 🔤 Request + Response Models
# -------------------------------

class PizzaRequest(BaseModel):
    question: str
    use_cloud_llm: bool = False

class PizzaResponse(BaseModel):
    answer: str
    sources: list[dict]  # each source is a dict with restaurant, city, etc.

class CacheStatsRequest(BaseModel):
    hours: int = 24

class CacheStatsResponse(BaseModel):
    message: str

class CachedEntry(BaseModel):
    question: str
    answer: str
    created_at: datetime

class CachedEntriesResponse(BaseModel):
    entries: List[CachedEntry]

# -------------------------------
# 🔁 API Routes
# -------------------------------

@app.post("/ask-pizza", response_model=PizzaResponse)
def ask_pizza(req: PizzaRequest):
    """
    POST /ask-pizza
    Generate an AI-powered pizza recommendation based on user input.

    Params:
    - question: The user's pizza-related query
    - use_cloud_llm: Toggle whether to use a cloud LLM

    Returns:
    - An answer string and a list of source reviews used in the response
    """
    try:
        answer, docs = get_pizza_answer(req.question, use_cloud_llm=req.use_cloud_llm)

        # Convert LangChain documents to dicts (for JSON-safe response)
        sources = []
        for doc in docs:
            sources.append({
                "restaurant": doc.metadata.get("restaurant", "N/A"),
                "city": doc.metadata.get("city", "N/A"),
                "rating": doc.metadata.get("rating", "N/A"),
                "date": doc.metadata.get("date", "N/A"),
                "review": doc.page_content
            })

        return PizzaResponse(answer=answer, sources=sources)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cache-stats", response_model=CacheStatsResponse, dependencies=[Depends(get_api_key)])
def get_stats(req: CacheStatsRequest):
    """
    POST /cache-stats [Admin Only]
    Get cache performance statistics for a specified time window.
    
    Requires admin API key in X-Admin-Key header.

    Params:
    - hours: Number of hours to look back (default: 24)

    Returns:
    - A message indicating stats were printed to console
    """
    try:
        message = get_cache_stats(req.hours)
        return CacheStatsResponse(message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cached-qa", response_model=CachedEntriesResponse, dependencies=[Depends(get_api_key)])
def get_cached_qa():
    """
    GET /cached-qa [Admin Only]
    Get all cached questions and answers, ordered by creation date (newest first).
    
    Requires admin API key in X-Admin-Key header.
    """
    entries = get_cached_entries()
    return {"entries": entries}

# -------------------------------
# 🔧 Local dev (optional)
# -------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
