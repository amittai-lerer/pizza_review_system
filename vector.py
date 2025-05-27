# """
# Pizza Review Vector Store
# ========================

# A semantic search system for pizza restaurant reviews using LangChain and ChromaDB.

# Features:
# ---------
# - Persistent vector storage with ChromaDB
# - High-quality embeddings using HuggingFace (BAAI/bge-small-en-v1.5)
# - City-based filtering and metadata-aware search
# - Automatic database initialization

# Example:
# --------
#     # Initialize retriever (creates DB if needed)
#     retriever = get_retriever(city="Tel Aviv")
    
#     # Search for reviews
#     results = retriever.invoke("best thin crust pizza")
# """

# import os
# from dataclasses import dataclass
# from typing import List, Optional

# import pandas as pd
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# import logging

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# )
# logger = logging.getLogger(__name__)

# @dataclass
# class VectorStoreConfig:
#     """Configuration settings for the vector store."""
#     csv_path: str = "data/final_israel_pizza_reviews_realistic.csv"
#     db_path: str = "chroma_langchain_db"
#     embedding_model: str = "BAAI/bge-small-en-v1.5"
#     collection_name: str = "restaurant_reviews"
#     results_per_query: int = 10

# class PizzaReviewVectorStore:
#     """Manages the vector store for pizza restaurant reviews."""
    
#     def __init__(self, config: VectorStoreConfig = VectorStoreConfig()):
#         self.config = config
#         self.embeddings = HuggingFaceEmbeddings(model_name=config.embedding_model)
#         self.vector_store = self._initialize_vector_store()
    
#     def _initialize_vector_store(self) -> Chroma:
#         """Initialize or load the vector store."""
#         if not os.path.exists(self.config.db_path):
#             return self._create_new_vector_store()
#         return self._load_existing_vector_store()
    
#     def _create_new_vector_store(self) -> Chroma:
#         """Create a new vector store from the CSV data."""
#         documents = self._prepare_documents()
#         logger.info(f"Creating vector store with {len(documents)} documents...")
        
#         vector_store = Chroma.from_documents(
#             documents=documents,
#             embedding=self.embeddings,
#             collection_name=self.config.collection_name,
#             persist_directory=self.config.db_path
#         )
#         logger.info("Vector store creation complete!")
#         return vector_store
    
#     def _load_existing_vector_store(self) -> Chroma:
#         """Load an existing vector store."""
#         return Chroma(
#             collection_name=self.config.collection_name,
#             persist_directory=self.config.db_path,
#             embedding_function=self.embeddings
#         )
    
#     def _prepare_documents(self) -> List[Document]:
#         """Prepare documents from CSV data for vector store creation."""
#         df = pd.read_csv(self.config.csv_path)
#         logger.info(f"Processing {len(df)} reviews...")
        
#         return [
#             Document(
#                 page_content=f"{row['Title']} {row['Review']}",
#                 metadata={
#                     "rating": float(row["Rating"]),
#                     "date": str(row["Date"]),
#                     "restaurant": row["Title"],
#                     "city": str(row["City"]).strip(),
#                     "state": str(row["State"]),
#                     "categories": str(row["Categories"])
#                 }
#             )
#             for _, row in df.iterrows()
#         ]
    
#     def get_retriever(self, city: Optional[str] = None):
#         """
#         Create a retriever for semantic search over pizza reviews.
        
#         Args:
#             city: Optional city name to filter results (case-insensitive)
        
#         Returns:
#             A configured LangChain retriever
#         """
#         search_kwargs = {"k": self.config.results_per_query}
        
#         if city:
#             normalized_city = city.strip()
#             search_kwargs["filter"] = {"city": normalized_city}
#             logger.info(f"Filtering by city: {normalized_city}")
#         else:
#             logger.info("No city filter applied")
        
#         retriever = self.vector_store.as_retriever(search_kwargs=search_kwargs)
#         logger.info(f"Retriever created with: {search_kwargs}")
#         return retriever

# # Initialize global vector store instance
# _vector_store = PizzaReviewVectorStore()

# def get_retriever(city: Optional[str] = None):
#     """
#     Public interface to get a retriever for pizza reviews.
#     Maintains backward compatibility with existing code.
#     """
#     return _vector_store.get_retriever(city)



"""
Pizza Review Vector Store
==========================

A semantic search system for pizza restaurant reviews using LangChain and ChromaDB.
"""

import os
import pandas as pd
from typing import Optional, List
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from logger_config import setup_logger


# --- Configuration ---
CSV_PATH = "data/final_israel_pizza_reviews_realistic.csv"
DB_PATH = "chroma_langchain_db"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
COLLECTION_NAME = "restaurant_reviews"
RESULTS_K = 10

# --- Logging ---
logger = setup_logger(name="vector", log_file="logs/vector.log")

# --- Load embedding model ---
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# --- Build vector DB if needed ---
def _create_documents_from_csv(csv_path: str) -> List[Document]:
    if not os.path.exists(csv_path):
        logger.error(f"CSV file not found: {csv_path}")
        raise FileNotFoundError(csv_path)

    df = pd.read_csv(csv_path)
    logger.info(f"🧾 Loading {len(df)} pizza reviews from CSV")

    docs = []
    for i, row in df.iterrows():
        try:
            doc = Document(
                page_content=f"{row['Title']} {row['Review']}",
                metadata={
                    "rating": float(row["Rating"]),
                    "date": str(row["Date"]),
                    "restaurant": row["Title"],
                    "city": str(row["City"]).strip(),
                    "state": str(row["State"]),
                    "categories": str(row["Categories"])
                }
            )
            docs.append(doc)
        except Exception as e:
            logger.warning(f"⚠️ Skipping row {i}: {e}")
    return docs

def _create_or_load_vector_store() -> Chroma:
    if not os.path.exists(DB_PATH):
        logger.info("📦 Vector DB not found, creating new one...")
        docs = _create_documents_from_csv(CSV_PATH)
        return Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=DB_PATH
        )
    else:
        logger.info("📂 Loading existing vector DB")
        return Chroma(
            collection_name=COLLECTION_NAME,
            persist_directory=DB_PATH,
            embedding_function=embeddings
        )

# --- Shared store instance ---
vector_store = _create_or_load_vector_store()

# --- Main retriever function ---
def get_retriever(city: Optional[str] = None):
    search_kwargs = {"k": RESULTS_K}
    if city:
        search_kwargs["filter"] = {"city": city.strip()}
        logger.info(f"🌍 Filtering by city: {city.strip()}")
    else:
        logger.info("🌍 No city filter applied")

    retriever = vector_store.as_retriever(search_kwargs=search_kwargs)
    logger.info(f"🔍 Retriever created with: {search_kwargs}")
    return retriever
