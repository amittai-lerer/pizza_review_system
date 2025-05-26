# --- core.py ---
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever
from llm_loader import get_llm_response

import os

# Prompt templates
rewrite_template = ChatPromptTemplate.from_template("""
You are a helpful assistant preparing a question for semantic search.

Do TWO things:
1. Normalize the city name (e.g., "TLV" → "Tel Aviv"). Return empty if no city is found.
2. Rewrite the user's question as if it were a sentence from a review.

Return in this format:
City: <normalized city>
Rewritten: <review-style version>

Question: {question}
""")

answer_template = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions about pizza restaurants in Israeli cities, based on real customer reviews.

Instructions:
- Add location to the answer.
- Use only relevant information from the reviews.
- Recommend 1–2 standout pizza places if appropriate.
- If no relevant reviews exist, say so clearly and politely.

Here are the reviews:
{reviews}

Question: {question}
""")

def get_answer_from_llm(prompt: str, mode: str) -> str:
    """Wrapper to handle LLM response for answer generation"""
    try:
        return get_llm_response(prompt, mode=mode)
    except Exception as e:
        if mode == "local":
            raise
        return get_llm_response(prompt, mode="cloud")

def get_pizza_answer(question: str, mode: str = "auto") -> tuple[str, list, str]:
    try:
        # LLM to rewrite query
        rewrite_output = get_llm_response(rewrite_template.format(question=question), mode=mode)
        used_mode = mode if mode != "auto" else "local"
    except Exception as e:
        if mode == "local":
            raise
        rewrite_output = get_llm_response(rewrite_template.format(question=question), mode="cloud")
        used_mode = "cloud"

    # Parse city and rewritten query
    lines = [line.strip() for line in rewrite_output.splitlines()]
    city, rewritten_query = "", ""
    for line in lines:
        if line.lower().startswith("city:"):
            city = line.split(":", 1)[1].strip()
        elif line.lower().startswith("rewritten:"):
            rewritten_query = line.split(":", 1)[1].strip()

    retriever = get_retriever(city if city else None)
    docs = retriever.invoke(rewritten_query)

    formatted_reviews = "\n\n".join([
        f"Review {i+1}:\n"
        f"Restaurant: {doc.metadata.get('restaurant', 'N/A')}\n"
        f"City: {doc.metadata.get('city', 'N/A')}, State: {doc.metadata.get('state', '')}\n"
        f"Categories: {doc.metadata.get('categories', '')}\n"
        f"Rating: {doc.metadata['rating']}\n"
        f"Date: {doc.metadata['date']}\n"
        f"Review:\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ]) if docs else "No relevant reviews found."

    # Get final answer using the same LLM mode
    answer = get_answer_from_llm(
        answer_template.format(reviews=formatted_reviews, question=question),
        mode=used_mode
    )

    return answer, docs, used_mode
