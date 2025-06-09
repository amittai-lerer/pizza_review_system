# --- api.py ---
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.core import get_pizza_answer  # make sure this is correct
import uvicorn

app = FastAPI()

# -------------------------------
# 🔤 Request + Response Models
# -------------------------------

class PizzaRequest(BaseModel):
    question: str
    use_cloud_llm: bool = False

class PizzaResponse(BaseModel):
    answer: str
    sources: list[dict]  # each source is a dict with restaurant, city, etc.

# -------------------------------
# 🔁 API Route
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

# -------------------------------
# 🔧 Local dev (optional)
# -------------------------------

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
