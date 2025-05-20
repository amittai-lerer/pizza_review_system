"""
Israeli Pizza Review Vector Store Setup
=======================================

This script creates or loads a persistent vector store using LangChain and ChromaDB
for semantic search over pizza restaurant reviews in Israeli cities.

Key Components:
---------------
- CSV Loader: Parses review data from a structured CSV file
- Ollama Embeddings: Converts text into high-dimensional vectors using `mxbai-embed-large`
- Chroma Vector Store: Stores vectors and enables fast metadata-filtered retrieval

Usage:
------
1. Ensure `dummy_israel_pizza_reviews.csv` is present in the data folder.
2. Run this script once to create the vector store.
3. Reuse the retriever in your main RAG pipeline via `get_retriever(city)`.
"""

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Step 1: Load review data from CSV
csv_path = "data/final_israel_pizza_reviews_realistic.csv"
df = pd.read_csv(csv_path)

# Step 2: Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# Step 3: Configure database location
DB_PATH = "chroma_langchain_db"
add_documents = not os.path.exists(DB_PATH)

# Step 4: Prepare documents for indexing
# Only prepare if we're creating the vector DB for the first time
documents = []
if add_documents:
    for i, row in df.iterrows():
        city = str(row["City"]).strip()
        doc = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={
                "rating": float(row["Rating"]),
                "date": str(row["Date"]),
                "restaurant": row["Title"],
                "city": city,
                "state": str(row["State"]),
                "categories": str(row["Categories"])
            }
        )
        documents.append(doc)

# Step 5: Create or load Chroma vector store
if add_documents:
    print(f"\U0001F4E6 Adding {len(documents)} documents to Chroma...")
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="restaurant_reviews",
        persist_directory=DB_PATH
    )
    print("\u2705 Vector store creation complete.")
else:
    vector_store = Chroma(
        collection_name="restaurant_reviews",
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

# Step 6: Retriever access function
def get_retriever(city=None):
    """
    Returns a retriever for semantically searching pizza reviews.
    Optionally filters results by city name (as found in the metadata).

    Args:
        city (str): Name of the city to filter by (e.g., "Tel Aviv")

    Returns:
        BaseRetriever: LangChain-compatible retriever object
    """
    search_kwargs = {"k": 10}
    if city:
        search_kwargs["filter"] = {"city": city.strip()}
    return vector_store.as_retriever(search_kwargs=search_kwargs)