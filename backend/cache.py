"""
Pizza Query Cache
================

A semantic caching system for pizza-related queries using SQLite and HuggingFace embeddings.

Key Features:
- Semantic matching using cosine similarity
- Automatic cache cleanup and size management
- Query filtering based on relevance
- Hit count tracking and performance metrics

Cache Rules:
- Max entries: 1000
- TTL: 7 days
- Min query length: 4 words
- Similarity threshold: 0.92

Usage:
    from backend.cache import get_cached_response, cache_response
    
    # Try to get cached response
    if cached := get_cached_response("best pizza in tel aviv"):
        answer, sources = cached
        return answer
        
    # Cache new response
    cache_response(question, answer, sources)
"""

from typing import Optional, Tuple, List
import sqlite3
import json
import time
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from logger_config import setup_logger
from backend.cache_metrics import MetricsTracker

# --- Configuration ---
CACHE_DIR = Path("cache")
DB_PATH = CACHE_DIR / "pizza_cache.db"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"  # Same as vector.py for consistency
SIMILARITY_THRESHOLD = 0.92  # Minimum cosine similarity to consider cache hit
CACHE_TTL_DAYS = 7  # Cache entries expire after 7 days
MAX_CACHE_ENTRIES = 1000  # Maximum number of cached entries
MIN_QUERY_LENGTH = 4  # Minimum number of words in query to cache
CACHE_CLEANUP_THRESHOLD = 0.8  # When cache reaches 80% capacity, cleanup old entries

# --- Setup ---
logger = setup_logger(name="cache", log_file="logs/cache.log")
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
metrics = MetricsTracker(DB_PATH)

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def should_cache_query(question: str) -> bool:
    """
    Determine if a query should be cached based on heuristics.
    
    Rules:
    - Min 4 words
    - Contains pizza-related keywords
    - Not too specific (no order numbers, addresses)
    
    Returns:
        bool: True if query should be cached
    """
    words = question.lower().split()
    
    # Check minimum length
    if len(words) < MIN_QUERY_LENGTH:
        logger.info("❌ Query too short for caching")
        return False
        
    # Check for relevant keywords
    relevant_keywords = {"pizza", "restaurant", "food", "delivery", "crust", "topping"}
    if not any(keyword in words for keyword in relevant_keywords):
        logger.info("❌ Query lacks relevant keywords for caching")
        return False
    
    # Avoid too specific queries
    specific_indicators = {"#", "order", "tracking", "address", "phone", "reservation"}
    if any(indicator in words for indicator in specific_indicators):
        logger.info("❌ Query too specific for caching")
        return False
    
    return True

def cleanup_cache():
    """
    Remove old/unused entries when cache nears capacity.
    
    Strategy:
    1. Remove expired entries (>7 days old)
    2. If still full, remove least recently used
    3. Maintains 60% of max capacity after cleanup
    """
    with sqlite3.connect(DB_PATH) as conn:
        # Get current cache size
        count = conn.execute("SELECT COUNT(*) FROM query_cache").fetchone()[0]
        
        if count >= MAX_CACHE_ENTRIES * CACHE_CLEANUP_THRESHOLD:
            logger.info("🧹 Running cache cleanup...")
            
            # Delete expired entries
            expiry = datetime.now() - timedelta(days=CACHE_TTL_DAYS)
            conn.execute("DELETE FROM query_cache WHERE created_at < ?", (expiry,))
            
            # If still too many entries, remove least recently used
            count = conn.execute("SELECT COUNT(*) FROM query_cache").fetchone()[0]
            if count >= MAX_CACHE_ENTRIES * CACHE_CLEANUP_THRESHOLD:
                to_delete = count - int(MAX_CACHE_ENTRIES * 0.6)  # Keep 60% of max
                conn.execute("""
                    DELETE FROM query_cache 
                    WHERE id IN (
                        SELECT id FROM query_cache 
                        ORDER BY created_at ASC 
                        LIMIT ?
                    )
                """, (to_delete,))
            
            conn.commit()
            logger.info(f"✨ Cache cleaned up. New size: {conn.execute('SELECT COUNT(*) FROM query_cache').fetchone()[0]}")

def init_cache():
    """
    Initialize the cache database with required tables.
    Handles schema migrations for new columns.
    """
    CACHE_DIR.mkdir(exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as conn:
        # Create table if it doesn't exist
        conn.execute("""
        CREATE TABLE IF NOT EXISTS query_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            question_embedding BLOB NOT NULL,
            answer TEXT NOT NULL,
            sources TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Check if hit_count column exists
        cursor = conn.execute("PRAGMA table_info(query_cache)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Add hit_count column if it doesn't exist
        if 'hit_count' not in columns:
            logger.info("Adding hit_count column to cache table")
            conn.execute("""
            ALTER TABLE query_cache 
            ADD COLUMN hit_count INTEGER DEFAULT 1
            """)
            
        conn.commit()
    logger.info("✅ Cache database initialized")

def get_cached_response(question: str) -> Optional[Tuple[str, List[Document]]]:
    """
    Find semantically similar cached response.
    
    Args:
        question: User query to find in cache
        
    Returns:
        Tuple of (answer, sources) if similarity > 0.92
        None if no good match found
    """
    start_time = time.time()
    
    # Get embedding for current question
    question_embedding = embeddings.embed_query(question)
    
    with sqlite3.connect(DB_PATH) as conn:
        # Get recent cache entries
        expiry = datetime.now() - timedelta(days=CACHE_TTL_DAYS)
        cursor = conn.execute(
            "SELECT id, question, answer, sources, question_embedding FROM query_cache WHERE created_at > ?",
            (expiry,)
        )
        
        best_match = None
        highest_similarity = 0
        best_match_id = None
        
        for row in cursor:
            entry_id, cached_q, answer, sources_json, embedding_bytes = row
            cached_embedding = json.loads(embedding_bytes)
            
            # Calculate cosine similarity
            similarity = cosine_similarity(question_embedding, cached_embedding)
            
            if similarity > highest_similarity and similarity >= SIMILARITY_THRESHOLD:
                highest_similarity = similarity
                best_match = (answer, sources_json)
                best_match_id = entry_id
        
        if best_match:
            answer, sources_json = best_match
            sources = [
                Document(page_content=s["content"], metadata=s["metadata"])
                for s in json.loads(sources_json)
            ]
            
            # Update hit count
            conn.execute(
                "UPDATE query_cache SET hit_count = hit_count + 1 WHERE id = ?",
                (best_match_id,)
            )
            conn.commit()
            
            time_saved = time.time() - start_time
            metrics.record_query(
                query=question,
                cache_hit=True,
                similarity=highest_similarity,
                time_saved_ms=time_saved * 1000
            )
            logger.info(f"✨ Cache hit! Similarity: {highest_similarity:.3f}")
            return answer, sources
    
    metrics.record_query(
        query=question,
        cache_hit=False,
        similarity=0.0,
        time_saved_ms=0.0
    )        
    logger.info("❌ Cache miss")
    return None

def cache_response(question: str, answer: str, sources: List[Document]):
    """
    Cache a new Q&A pair if it meets criteria.
    
    Args:
        question: Original query
        answer: Generated response
        sources: Source documents used
        
    Note:
        Automatically handles cleanup if cache is full
    """
    if not should_cache_query(question):
        logger.info("⏭️ Skipping cache for this query")
        return
        
    # Check and cleanup cache if needed
    cleanup_cache()
    
    # Convert question to embedding
    question_embedding = embeddings.embed_query(question)
    
    # Convert sources to JSON-serializable format
    sources_json = json.dumps([
        {
            "content": doc.page_content,
            "metadata": doc.metadata
        }
        for doc in sources
    ])
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO query_cache 
                (question, question_embedding, answer, sources)
            VALUES 
                (?, ?, ?, ?)
            """,
            (
                question,
                json.dumps(question_embedding),
                answer,
                sources_json
            )
        )
        conn.commit()
    logger.info("💾 Response cached successfully")

def get_cached_entries() -> List[dict]:
    """
    Get all cached Q&As with metadata.
    
    Returns:
        List of dicts with:
        - question: Original query
        - answer: Cached response
        - created_at: Timestamp
        - hit_count: Times accessed
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute(
            """
            SELECT question, answer, created_at, hit_count 
            FROM query_cache 
            ORDER BY created_at DESC
            """
        )
        
        entries = []
        for row in cursor:
            entries.append({
                "question": row[0],
                "answer": row[1],
                "created_at": row[2],
                "hit_count": row[3]
            })
        
        return entries

def get_cache_stats(hours: int = 24) -> str:
    """Get a formatted report of cache performance statistics."""
    metrics.print_report(hours)
    return "Cache statistics printed to console"

# Initialize cache on module import
init_cache() 