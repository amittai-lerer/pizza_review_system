# --- core.py ---
import os
from typing import Optional, List, Tuple

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from vector import get_retriever
from llm_loader import get_llm_response
from logger_config import setup_logger

logger = setup_logger()

# --- Prompt templates ---
rewrite_template = ChatPromptTemplate.from_template("""
You are a helpful assistant preparing a user query for semantic search on pizza reviews.

DO TWO THINGS:
1. If the city is explicitly mentioned (e.g., "Jerusalem", "TLV", "Haifa"), normalize it to its full name (e.g., "TLV" → "Tel Aviv"). Only extract the city if it is clearly and directly stated. DO NOT guess or assume a city from context or wording.
2. Rewrite the user's question into a sentence that sounds like a review someone might write after visiting a pizza place.

IMPORTANT:
- If the city is NOT mentioned in the question, return: City: no city found
- Do NOT invent or infer locations.
- Follow the exact format below.

Return ONLY in this exact format (no extra text):

City: <normalized city or "no city found">
Rewritten: <review-style sentence>

Examples:

Question: Where can I get spicy pizza in TLV?
City: Tel Aviv
Rewritten: I had an amazing spicy pizza in Tel Aviv.

Question: Best pizza crust
City: no city found
Rewritten: I'm looking for pizza places that have the best crust.

Now process the following question:
Question: {question}
""")


answer_template = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions about pizza restaurants in Israeli cities,
based on real customer reviews.

Instructions:
- Add location to the answer.
- Use only relevant information from the reviews.
- Recommend 1–2 standout pizza places if appropriate.
- If no relevant reviews exist, say so clearly and politely.

Here are the reviews:
{reviews}

Question: {question}
""")


def rewrite_question_and_extract_city(question: str, mode: str) -> Tuple[str, str, str]:
    try:
        logger.info(f"🔁 Rewriting input question: {question}")
        rewrite_output = get_llm_response(rewrite_template.format(question=question), mode=mode)
        used_mode = mode if mode != "auto" else "local"
    except Exception as e:
        logger.warning(f"⚠️ Local LLM failed. Falling back to cloud: {e}")
        rewrite_output = get_llm_response(rewrite_template.format(question=question), mode="cloud")
        used_mode = "cloud"

    logger.debug(f"🧾 Rewrite Output:\n{rewrite_output}")

    city, rewritten_query = "", ""
    for line in rewrite_output.splitlines():
        line = line.strip()
        if line.lower().startswith("city:"):
            city = line.split(":", 1)[1].strip()
            if "no city found" in city.lower():
                city = ""
        elif line.lower().startswith("rewritten:"):
            rewritten_query = line.split(":", 1)[1].strip()

    logger.info(f"🔍 Parsed City: {city or '[None]'}")
    logger.info(f"📝 Rewritten Query: {rewritten_query}")
    return city, rewritten_query, used_mode


def retrieve_relevant_reviews(query: str, city: Optional[str]) -> List[Document]:
    logger.info(f"🌍 Filtering by city: {city or '[None]'}")
    retriever = get_retriever(city if city else None)
    logger.debug(f"🔧 Retriever initialized with search query: {query}")
    return retriever.invoke(query)


def format_reviews_for_prompt(docs: List[Document]) -> str:
    if not docs:
        logger.warning("📭 No documents found for query.")
        return "No relevant reviews found."

    logger.info(f"📚 Formatting {len(docs)} retrieved reviews.")
    return "\n\n".join([
        f"Review {i+1}:\n"
        f"Restaurant: {doc.metadata.get('restaurant', 'N/A')}\n"
        f"City: {doc.metadata.get('city', 'N/A')}, State: {doc.metadata.get('state', '')}\n"
        f"Categories: {doc.metadata.get('categories', '')}\n"
        f"Rating: {doc.metadata['rating']}\n"
        f"Date: {doc.metadata['date']}\n"
        f"Review:\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])


def get_answer_from_llm(prompt: str, mode: str) -> str:
    try:
        logger.info(f"✍️ Generating final answer with mode: {mode}")
        logger.info("--------------------------------")
        return get_llm_response(prompt, mode=mode)
    except Exception as e:
        logger.error(f"❌ Failed in local mode. Retrying in cloud mode. Error: {e}")
        return get_llm_response(prompt, mode="cloud")


def get_pizza_answer(question: str, mode: str = "auto") -> tuple[str, list, str]:
    city, rewritten_query, used_mode = rewrite_question_and_extract_city(question, mode)
    docs = retrieve_relevant_reviews(rewritten_query, city)
    formatted_reviews = format_reviews_for_prompt(docs)
    answer = get_answer_from_llm(answer_template.format(reviews=formatted_reviews, question=question), mode=used_mode)
    return answer, docs, used_mode
