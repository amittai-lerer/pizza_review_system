
# """
# Pizza Review Q&A System
# ========================

# A sophisticated question-answering system for pizza restaurant reviews using:
# - LangChain for orchestrating the Q&A pipeline
# - Ollama (Llama 3.2) for local LLM inference
# - ChromaDB for efficient vector-based retrieval
# - HuggingFace embeddings for semantic search

# Usage:
# ------
# Run this script in the terminal:
# $ python main.py

# Or import and use the function `get_pizza_answer(question)` in a Streamlit dashboard or other UI.
# """

# from langchain_ollama.llms import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# from vector import get_retriever

# # Step 1: Combined Prompt to Normalize City and Rewrite Query
# rewrite_template = ChatPromptTemplate.from_template("""
# You are a helpful assistant preparing a question for semantic search.

# Do TWO things:
# 1. Normalize the city name (e.g., "TLV" → "Tel Aviv"). Return empty if no city is found.
# 2. Rewrite the user's question as if it were a sentence from a review.

# Examples:
# - "Where to eat in TLV?" → City: Tel Aviv, Rewritten: The pizza in Tel Aviv was delicious and crispy.
# - "Best pizza near Al-Quds?" → City: Jerusalem, Rewritten: I had the best pizza near Jerusalem.
# - "Where can I find good crust?" → City: , Rewritten: The crust was crispy and perfectly baked.

# Return in this format:
# City: <normalized city>
# Rewritten: <review-style version>

# Question: {question}
# """)

# # Step 2: Answer Generation Prompt
# answer_template = ChatPromptTemplate.from_template("""
# You are a helpful assistant answering questions about pizza restaurants in Israeli cities, based on real customer reviews.

# Your tone is friendly and natural — like you're giving useful advice to a friend. Stay on topic and answer only what the user asks.

# Instructions:
# - Focus on answering the specific question asked.
# - Add location to the answer
# - Use only relevant information from the reviews.
# - Recommend 1–2 standout pizza places if appropriate.
# - Highlight what makes them great (crust, flavor, service, etc.) — but keep it concise.
# - Avoid listing every review or going off-topic.
# - If no relevant reviews exist, say so clearly and politely.

# Here are the reviews:
# {reviews}

# Question: {question}
# """)

# # Step 3: Initialize Ollama LLM
# model = OllamaLLM(model="llama3.2")

# # Step 4: Create LangChain chains
# rewrite_chain = rewrite_template | model
# answer_chain = answer_template | model


# # ✅ Step 5: Modular function to reuse in CLI or Streamlit
# def get_pizza_answer(user_question: str):
#     """
#     Full Q&A pipeline for pizza review system.
#     Returns:
#         - answer (str)
#         - city (str): Normalized city
#         - rewritten_query (str): Reformatted query for vector search
#         - formatted_reviews (str): Formatted context sent to LLM
#     """
#     rewrite_output = rewrite_chain.invoke({"question": user_question})
#     lines = [line.strip() for line in rewrite_output.splitlines()]
#     city = ""
#     rewritten_query = ""

#     for line in lines:
#         if line.lower().startswith("city:"):
#             city = line.split(":", 1)[1].strip()
#         elif line.lower().startswith("rewritten:"):
#             rewritten_query = line.split(":", 1)[1].strip()

#     retriever = get_retriever(city if city else None)
#     retrieved_docs = retriever.invoke(rewritten_query)

#     formatted_reviews = "\n\n".join([
#         f"Review {i+1}:\n"
#         f"Restaurant: {doc.metadata.get('restaurant', 'N/A')}\n"
#         f"City: {doc.metadata.get('city', 'N/A')}, State: {doc.metadata.get('state', '')}\n"
#         f"Categories: {doc.metadata.get('categories', '')}\n"
#         f"Rating: {doc.metadata['rating']}\n"
#         f"Date: {doc.metadata['date']}\n"
#         f"Review:\n{doc.page_content}"
#         for i, doc in enumerate(retrieved_docs)
#     ]) if retrieved_docs else "No relevant reviews found."

#     answer = answer_chain.invoke({
#         "reviews": formatted_reviews,
#         "question": user_question
#     })

#     return answer, city, rewritten_query, formatted_reviews


# # ✅ Step 6: Terminal-based loop (still works!)
# if __name__ == "__main__":
#     while True:
#         question = input("\nPlease enter your pizza-related question (or 'q' to quit): ").strip()
#         if question.lower() == "q":
#             print("Goodbye! 🍕")
#             break

#         answer, city, rewritten, reviews = get_pizza_answer(question)

        
#         print("\nAnswer:\n--------")
#         print(answer)
#         print("\n--------------------------------")






from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever

# Import shared function
from core import get_pizza_answer

if __name__ == "__main__":
    while True:
        question = input("\nPlease enter your pizza-related question (or 'q' to quit): ").strip()
        if question.lower() == "q":
            print("Goodbye! 🍕")
            break

        # Use shared function to process and answer
        answer , _ = get_pizza_answer(question)
        print("\nAnswer:\n--------")
        print(answer)
        print("\n--------------------------------")
