"""
Vector Store Implementation for Pizza Reviews
==========================================

A semantic search system that converts restaurant reviews into vector embeddings
for efficient similarity search. This enables finding relevant reviews for any question.

System Components & Flow:
1. Data Loading:
   - Reads restaurant reviews from CSV
   - Processes text and metadata (ratings, dates)
   - Creates LangChain Document objects

2. Vector Processing:
   - Uses Ollama embeddings to convert text to vectors
   - Stores vectors in ChromaDB for efficient retrieval
   - Provides a retriever interface for semantic search

3. Persistence:
   - Saves vectors to disk for reuse
   - Avoids reprocessing on subsequent runs
   - Maintains vector database in 'chroma_langchain_db'

Technical Details:
- Embedding Model: mxbai-embed-large (optimized for semantic search)
- Vector Store: ChromaDB (efficient similarity search)
- Document Format: LangChain Documents with metadata
- Search Config: Top-5 most relevant results

Integration with main.py:
- Exposes 'retriever' object for semantic search
- Returns Document objects with review content and metadata
- Enables semantic matching between questions and reviews
"""

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Step 1: Load and prepare review data
try:
    # Read reviews from CSV file
    df = pd.read_csv("realistic_restaurant_reviews.csv")
except Exception as e:
    raise

# Step 2: Initialize embedding model for vector conversion
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Step 3: Configure vector store settings
db_location = "chroma_langchain_db"
# Check if we need to create new vectors or can load existing ones
add_documents = not os.path.exists(db_location)

# Step 4: Process documents if this is first run
if add_documents:
    documents = []
    ids = []
    for i, row in df.iterrows():
        # Combine title and review for better semantic context
        # Create Document objects with content and searchable metadata
        document = Document(
            page_content=row["Title"] + " " + row["Review"],
            metadata={"rating": row["Rating"], "date": row["Date"], "title": row["Title"]}
        )
        ids.append(str(i))
        documents.append(document)


# Step 5: Initialize or load the vector store
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

# Step 6: Add documents to vector store if new database
if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
    vector_store.persist()  # Save vectors to disk

# Step 7: Create and expose the retriever interface
# This is the main integration point with main.py
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}  # Return top 5 most relevant results
)




