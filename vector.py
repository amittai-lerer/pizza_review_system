"""
Pizza Review Vector Store Implementation
======================================

This module implements a persistent vector store for pizza restaurant reviews using:
- HuggingFace Embeddings (BAAI/bge-small-en-v1.5) for high-quality text embeddings
- ChromaDB for efficient vector storage and retrieval
- Pandas for structured data handling
- LangChain for seamless integration with the Q&A pipeline

Key Features:
------------
1. Persistent Storage:
   - Reviews are embedded and stored in ChromaDB
   - Automatic initialization on first run
   - Efficient incremental updates

2. Metadata Integration:
   - Rich metadata storage (ratings, dates, categories)
   - City-based filtering
   - Full review text preservation

3. Retrieval System:
   - Semantic similarity search
   - Configurable result count
   - Metadata-filtered queries

Usage:
------
1. First-time setup:
   ```python
   # Will create the vector store if it doesn't exist
   from vector import get_retriever
   retriever = get_retriever()
   ```

2. Subsequent usage:
   ```python
   # Optional city filtering
   retriever = get_retriever(city="New York")
   results = retriever.invoke("great thin crust pizza")
   ```

File Structure:
--------------
Expected data file: data/combined_reviews.csv
Vector store location: chroma_langchain_db/
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Configuration Constants
CSV_PATH = CSV_PATH = "data/final_israel_pizza_reviews_realistic.csv"
DB_PATH = "chroma_langchain_db"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "restaurant_reviews"

# Initialize embedding model with high-quality embeddings
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Check if we need to create a new vector store
add_documents = not os.path.exists(DB_PATH)

# Document preparation for initial vector store creation
documents = []
if add_documents:
    # Load and process review data
    df = pd.read_csv(CSV_PATH)
    
    print(f"\U0001F4DD Processing {len(df)} reviews...")
    for i, row in df.iterrows():
        # Create document with comprehensive metadata
        doc = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={
                "rating": float(row["Rating"]),
                "date": str(row["Date"]),
                "restaurant": row["Title"],
                "city": str(row["City"]).strip(),
                "state": str(row["State"]),
                "categories": str(row["Categories"])
            }
        )
        documents.append(doc)

# Vector store initialization or loading
if add_documents:
    print(f"\U0001F4E6 Creating vector store with {len(documents)} documents...")
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH
    )
    print("\u2705 Vector store creation complete!")
else:
    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

def get_retriever(city=None):
    """
    Creates a retriever for semantic search over pizza reviews with optional city filtering.

    Args:
        city (str, optional): City name to filter results by. Case-insensitive.
                            If None, searches across all cities.

    Returns:
        BaseRetriever: A LangChain retriever configured for:
            - Top 10 most relevant results
            - Optional city-based filtering
            - Metadata-aware search

    Example:
        >>> retriever = get_retriever(city="New York")
        >>> results = retriever.invoke("best thin crust pizza")
    """
    search_kwargs = {"k": 10}  # Return top 10 results
    if city:
        search_kwargs["filter"] = {"city": city.strip()}
    return vector_store.as_retriever(search_kwargs=search_kwargs)