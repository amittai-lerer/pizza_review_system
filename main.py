"""
Pizza Restaurant Review Analysis System
=====================================

A question-answering system that analyzes pizza restaurant reviews using LangChain and Ollama.
The system uses a local LLM to provide intelligent answers about restaurant reviews.

System Components & Flow:
1. Vector Store (vector.py):
   - Loads reviews from CSV
   - Creates embeddings using Ollama
   - Stores vectors in ChromaDB for semantic search

2. Main QA System (main.py):
   - Uses Ollama LLM for text generation
   - Retrieves relevant reviews using vector similarity
   - Processes questions through a structured prompt
   - Returns concise, relevant answers

Technical Flow:
1. User inputs a question
2. Vector store finds relevant reviews (semantic search)
3. Reviews are formatted and sent to LLM
4. LLM generates a concise, contextual answer

Requirements:
- Ollama with llama3.2 model
- langchain-ollama
- langchain-core
- ChromaDB for vector storage
"""

from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever  # Custom vector store implementation

# Initialize Ollama LLM - This is our text generation engine
model = OllamaLLM(model="llama3.2")

# Define how the AI should process questions and reviews
# This template structures the AI's responses for consistency
template = """
You are a helpful assistant that can answer questions and help with tasks.
You're an expert in the field of pizza restaurants.

Here are the relevant reviews I found:
{reviews}

Based on these reviews, please answer the following question: {question}

Remember to:
1. Only use information from the provided reviews
2. If the reviews don't contain relevant information, say so
3. Be specific and cite details from the reviews when possible
4. answer short and concise
"""

# Create prompt template for consistent AI interactions
prompt = ChatPromptTemplate.from_template(template)

# Combine prompt and model into a processing chain
# This creates our question-answering pipeline
chain = prompt | model

# Main interaction loop
while True:
    print("\n\n\n--------------------------------")
    question = input("Please enter your question: (or type q to quit) ")
    print("--------------------------------\n\n\n")
    if question == "q":
        break
    
    # Step 1: Retrieve relevant reviews using semantic search
    retrieved_docs = retriever.get_relevant_documents(question)
    
    # Step 2: Format reviews for the AI prompt
    # Each review includes its content, rating, and date
    formatted_reviews = "\n\n".join([
        f"Review {i+1}:\n{doc.page_content}\nRating: {doc.metadata['rating']}\nDate: {doc.metadata['date']}"
        for i, doc in enumerate(retrieved_docs)
    ])
    
    print(f"📚 Found {len(retrieved_docs)} relevant reviews...")
    
    # Step 3: Process question through our AI chain
    # The chain combines the reviews, question, and AI model
    result = chain.invoke({
                             "reviews": formatted_reviews if retrieved_docs else "No relevant reviews found.",
                             "question": question
    })
    
    # Step 4: Display the AI's response
    print("\n🤖 Answer:")
    print(result)
    