
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
