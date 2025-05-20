# core.py
"""
Shared logic for pizza review Q&A system.
This module handles:
- LLM initialization
- Prompt chains
- Answer generation
- Retrieval logic
"""

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever

# --- Prompt for normalizing and rewriting the query ---
rewrite_template = ChatPromptTemplate.from_template("""
You are a helpful assistant preparing a question for semantic search.

Do TWO things:
1. Normalize the city name (e.g., "TLV" → "Tel Aviv"). Return empty if no city is found.
2. Rewrite the user's question as if it were a sentence from a review.

Examples:
- "Where to eat in TLV?" → City: Tel Aviv, Rewritten: The pizza in Tel Aviv was delicious and crispy.
- "Best pizza near Al-Quds?" → City: Jerusalem, Rewritten: I had the best pizza near Jerusalem.
- "Where can I find good crust?" → City: , Rewritten: The crust was crispy and perfectly baked.

Return in this format:
City: <normalized city>
Rewritten: <review-style version>

Question: {question}
""")

# --- Prompt for generating the final answer ---
answer_template = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions about pizza restaurants in Israeli cities, based on real customer reviews.

Your tone is friendly and natural — like you're giving useful advice to a friend. Stay on topic and answer only what the user asks.

Instructions:
- Focus on answering the specific question asked.
- Add location to the answer.
- Use only relevant information from the reviews.
- Recommend 1–2 standout pizza places if appropriate.
- Highlight what makes them great (crust, flavor, service, etc.) — but keep it concise.
- Avoid listing every review or going off-topic.
- If no relevant reviews exist, say so clearly and politely.

Here are the reviews:
{reviews}

Question: {question}
""")

# --- Initialize the model and chains ---
model = OllamaLLM(model="llama3.2")
rewrite_chain = rewrite_template | model
answer_chain = answer_template | model

# --- Exposed function for both CLI and dashboard ---
def get_pizza_answer(question: str) -> tuple[str, list]:
    rewrite_output = rewrite_chain.invoke({"question": question})
    lines = [line.strip() for line in rewrite_output.splitlines()]
    city = ""
    rewritten_query = ""

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

    answer = answer_chain.invoke({
        "reviews": formatted_reviews,
        "question": question
    })

    return answer, docs
