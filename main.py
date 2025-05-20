"""
Pizza Review Q&A System
======================

A sophisticated question-answering system for pizza restaurant reviews using:
- LangChain for orchestrating the Q&A pipeline
- Ollama (Llama 3.2) for local LLM inference
- ChromaDB for efficient vector-based retrieval
- HuggingFace embeddings for semantic search

Key Components:
--------------
1. Query Preprocessing:
   - City name normalization (e.g., "NYC" → "New York")
   - Query rewriting for optimal semantic matching
   - Metadata filtering setup

2. Document Retrieval:
   - City-filtered semantic search
   - Metadata-aware document ranking
   - Context window optimization

3. Answer Generation:
   - Context-aware response formulation
   - Location-specific recommendations
   - Natural, conversational tone

Usage:
------
Run the script directly:
```bash
python main.py
```

The system will start an interactive session where you can ask questions about pizza restaurants.
Type 'q' to exit the session.

Example Questions:
- "What are the best pizza places in Tel Aviv?"
- "Where can I find authentic New York style pizza?"
- "Tell me about kosher pizza options in Jerusalem"
"""

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import get_retriever

# Step 1: Combined Prompt to Normalize City and Rewrite Query
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

# Step 2: Answer Generation Prompt
answer_template = ChatPromptTemplate.from_template("""
You are a helpful assistant answering questions about pizza restaurants in Israeli cities, based on real customer reviews.

Your tone is friendly and natural — like you're giving useful advice to a friend. Stay on topic and answer only what the user asks.

Instructions:
- Focus on answering the specific question asked.
- Add location to the answer
- Use only relevant information from the reviews.
- Recommend 1–2 standout pizza places if appropriate.
- Highlight what makes them great (crust, flavor, service, etc.) — but keep it concise.
- Avoid listing every review or going off-topic.
- If no relevant reviews exist, say so clearly and politely.

Here are the reviews:
{reviews}

Question: {question}
""")

# Step 3: Initialize LLM with Ollama
model = OllamaLLM(model="llama3.2")

# Step 4: Create LangChain processing chains
rewrite_chain = rewrite_template | model  # Chain for query preprocessing
answer_chain = answer_template | model    # Chain for answer generation

# Step 5: Main Interactive Loop
if __name__ == "__main__":
    while True:
        # Get user input
        question = input("\nPlease enter your pizza-related question (or 'q' to quit): ").strip()
        if question.lower() == "q":
            print("Goodbye! 🍕")
            break

        # Process query through rewrite chain
        rewrite_output = rewrite_chain.invoke({"question": question})
        lines = [line.strip() for line in rewrite_output.splitlines()]
        city = ""
        rewritten_query = ""

        # Extract city and rewritten query
        for line in lines:
            if line.lower().startswith("city:"):
                city = line.split(":", 1)[1].strip()
            elif line.lower().startswith("rewritten:"):
                rewritten_query = line.split(":", 1)[1].strip()

        # Debug output
        print(f"Retriever filtering by city: {city if city else 'None (global search)'}")
        print(f"Query reformulated for embedding: {rewritten_query}")

        # Retrieve relevant documents
        retriever = get_retriever(city if city else None)
        retrieved_docs = retriever.invoke(rewritten_query)

        # Format retrieved documents for LLM context
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

        # Generate and display answer
        answer = answer_chain.invoke({
            "reviews": formatted_reviews,
            "question": question
        })

        print("\nAnswer:\n--------")
        print(answer)
        print("\n--------------------------------")
