# --- core.py ---
# This module handles LLM-based question rewriting, city extraction, vector retrieval, and final answer generation.

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever
from logger_config import setup_logger
import os

# --- Setup logger ---
logger = setup_logger(name="core", log_file="logs/core.log")

# --- Load Local LLM ---
llm = OllamaLLM(model="llama3.2")

# --- Prompt Templates ---
# Template that instructs the LLM to extract and normalize city names and rewrite vague questions.
rewrite_template = ChatPromptTemplate.from_template("""
You are a helpful assistant preparing a user query for semantic search on pizza reviews.

Your job has TWO steps:
1. Normalize city abbreviations to full names, using this list:
   - TLV → Tel Aviv
   - JLM → Jerusalem
   - Haifa → Haifa

   Only extract the city if it is **explicitly** mentioned. DO NOT guess or infer it.

2. Rewrite the user's question into a sentence that sounds like a review someone might write after visiting a pizza place.

Return your response **exactly** like this (no extra text):

City: <Tel Aviv / Jerusalem / Haifa / no city found>  
Rewritten: <review-style sentence>

Here are examples:

---
Question: Where can I find good pizza in TLV?  
City: Tel Aviv  
Rewritten: I found amazing pizza in Tel Aviv.

Question: I want the crispiest pizza crust.  
City: no city found  
Rewritten: I'm looking for pizza places with the crispiest crust.

Question: Best pizza in JLM?  
City: Jerusalem  
Rewritten: I had the best pizza experience in Jerusalem.

Now process this:  
Question: {question}
""")

# Template for final response generation using retrieved reviews
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

# --- Chains ---
# LangChain prompt pipelines for rewrite and answer generation
rewrite_chain = rewrite_template | llm
answer_chain = answer_template | llm

# --- Core Functions ---
def rewrite_and_extract_city(question: str) -> tuple[str, str]:
    """Rewrite the user's question and extract the normalized city name if present."""
    logger.info(f"🔁 Rewriting question: {question}")
    output = rewrite_chain.invoke({"question": question})
    logger.info(f"✅ LLM rewrite output:\n{output}")

    city, rewritten = "", ""
    for line in output.splitlines():
        if line.lower().startswith("city:"):
            value = line.split(":", 1)[1].strip()
            city = value if value.lower() != "no city found" else ""
        elif line.lower().startswith("rewritten:"):
            rewritten = line.split(":", 1)[1].strip()

    logger.info(f"🏩 Parsed city: {city or '[None]'}")
    logger.info(f"✍️ Rewritten query: {rewritten}")
    return city, rewritten

def format_reviews(docs: list) -> str:
    """Format retrieved documents for inclusion in the final prompt."""
    logger.info(f"📚 Formatting {len(docs)} reviews")
    if not docs:
        return "No relevant reviews found."

    return "\n\n".join([
        f"Review {i+1}:\n"
        f"Restaurant: {doc.metadata.get('restaurant', 'N/A')}\n"
        f"City: {doc.metadata.get('city', 'N/A')}\n"
        f"Rating: {doc.metadata.get('rating', 'N/A')}\n"
        f"Date: {doc.metadata.get('date', 'N/A')}\n"
        f"Review:\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])

def get_pizza_answer(question: str) -> tuple[str, list]:
    """Main handler that processes a user question and returns the final LLM-generated answer."""
    logger.info("🚀 Handling new pizza question")
    city, rewritten_query = rewrite_and_extract_city(question)

    logger.info(f"🔍 Retrieving docs for: '{rewritten_query}' (city={city or 'Any'})")
    retriever = get_retriever(city or None)
    docs = retriever.invoke(rewritten_query)

    reviews = format_reviews(docs)
    logger.info("🧠 Calling LLM to generate answer")
    answer = answer_chain.invoke({"reviews": reviews, "question": question})

    logger.info("✅ Answer ready")
    return answer, docs
