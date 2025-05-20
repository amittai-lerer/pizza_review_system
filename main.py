"""
Israeli Pizza Review Q&A System
==============================

A conversational system for exploring pizza restaurant reviews in Israeli cities using:
- LangChain for semantic search and prompt chaining
- Ollama (LLaMA 3.2) for local language model inference
- ChromaDB for vector-based document retrieval

Workflow:
---------
1. Accept a natural language question from the user (e.g., "What's a good pizza place in Tel Aviv?").
2. Use a local LLM to normalize city references to their canonical form (e.g., "TLV" → "Tel Aviv").
3. Retrieve semantically relevant reviews from ChromaDB filtered by that city.
4. Format and present those reviews to the LLM to generate a final answer.

Supports reviews from:
- Tel Aviv, Jerusalem, Haifa, Beer Sheva, Eilat
"""

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever

# Step 1: City Normalization Prompt Chain
rewrite_template = ChatPromptTemplate.from_template("""
You are a city name normalizer. Your ONLY job is to output the canonical city name mentioned in the question.

Rules:
- Output ONLY the normalized city name. No quotes, no explanation.
- If you find "TLV", "Tel Aviv-Jaffa", or variants → output "Tel Aviv".
- If no city is found → return an empty string.

Examples:
- "Where to eat in TLV?" → Tel Aviv
- "Best pizza near Al-Quds?" → Jerusalem
- "Pizza in haifa bay?" → Haifa

Question: {question}
""")


# Step 2: Answer Prompt Chain Template
answer_template = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions based on pizza restaurant reviews in Israeli cities.

Each review includes:
- Restaurant name
- City and state
- Rating and date
- Full review text

Instructions:
1. Recommend specific pizza places in the city mentioned.
2. Use restaurant name and city.
3. Mention why it's good (e.g., service, crust, taste).
4. Be brief, clear, and informative.
5. If no reviews for the city exist, say so.

Here are the reviews:
{reviews}

Question: {question}
""")

# Step 3: Initialize Ollama LLM
model = OllamaLLM(model="llama3.2")

# Step 4: Chain construction
rewrite_chain = rewrite_template | model
answer_chain = answer_template | model

# Step 5: Main user loop
if __name__ == "__main__":
    while True:
        question = input("\nPlease enter your pizza-related question (or 'q' to quit): ").strip()
        if question.lower() == "q":
            print("Goodbye! 🍕")
            break

        # Normalize city using LLM
        normalized_city = rewrite_chain.invoke({"question": question}).strip()
        city = normalized_city if normalized_city else None

        # Retrieve relevant documents using metadata filtering
        retriever = get_retriever(city)
        retrieved_docs = retriever.invoke(question)

        # Format documents for the answer prompt
        formatted_reviews = "\n\n".join([
            f"Review {i+1}:\n"
            f"Restaurant: {doc.metadata.get('restaurant', 'N/A')}\n"
            f"City: {doc.metadata.get('city', 'N/A')}, State: {doc.metadata.get('state', '')}\n"
            f"Categories: {doc.metadata.get('categories', '')}\n"
            f"Rating: {doc.metadata['rating']}\n"
            f"Date: {doc.metadata['date']}\n"
            f"Review:\n{doc.page_content}"
            for i, doc in enumerate(retrieved_docs)
        ]) if retrieved_docs else "No relevant reviews found."

        # Generate final answer
        answer = answer_chain.invoke({
            "reviews": formatted_reviews,
            "question": question
        })

        print("\nAnswer:\n--------")
        print(answer)
        print("\n--------------------------------")
