"""
Cache Metrics Tracker
===================

Tracks and reports performance metrics for the pizza query cache.
"""

from typing import Dict, List, Optional
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import json
from collections import Counter
from dataclasses import dataclass

@dataclass
class CacheMetrics:
    total_queries: int
    cache_hits: int
    cache_misses: int
    avg_similarity_score: float
    cache_size_bytes: int
    most_common_queries: List[tuple[str, int]]
    avg_response_time_saved_ms: float

class MetricsTracker:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._setup_metrics_table()

    def _setup_metrics_table(self):
        """Create metrics tracking table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS cache_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                query TEXT NOT NULL,
                cache_hit BOOLEAN NOT NULL,
                similarity_score FLOAT,
                response_time_saved_ms FLOAT
            )
            """)
            conn.commit()

    def record_query(self, query: str, cache_hit: bool, similarity: Optional[float] = None, time_saved_ms: Optional[float] = None):
        """Record metrics for a single query."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO cache_metrics (query, cache_hit, similarity_score, response_time_saved_ms)
                VALUES (?, ?, ?, ?)
                """,
                (query, cache_hit, similarity, time_saved_ms)
            )
            conn.commit()

    def get_metrics(self, time_window_hours: int = 24) -> CacheMetrics:
        """Get cache performance metrics for the specified time window."""
        since = datetime.now() - timedelta(hours=time_window_hours)
        
        with sqlite3.connect(self.db_path) as conn:
            # Get basic stats
            cursor = conn.execute(
                """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN cache_hit THEN 1 ELSE 0 END) as hits,
                    AVG(CASE WHEN cache_hit THEN similarity_score ELSE 0 END) as avg_sim,
                    AVG(CASE WHEN cache_hit THEN response_time_saved_ms ELSE 0 END) as avg_time
                FROM cache_metrics 
                WHERE timestamp > ?
                """,
                (since,)
            )
            row = cursor.fetchone()
            total = row[0]
            hits = row[1] or 0
            avg_sim = row[2] or 0.0
            avg_time_saved = row[3] or 0.0

            # Get most common queries
            cursor = conn.execute(
                """
                SELECT query, COUNT(*) as count 
                FROM cache_metrics 
                WHERE timestamp > ?
                GROUP BY query 
                ORDER BY count DESC 
                LIMIT 5
                """,
                (since,)
            )
            common_queries = cursor.fetchall()

            # Calculate cache size
            cursor = conn.execute(
                "SELECT SUM(LENGTH(question_embedding) + LENGTH(answer) + LENGTH(sources)) FROM query_cache"
            )
            cache_size = cursor.fetchone()[0] or 0

        return CacheMetrics(
            total_queries=total,
            cache_hits=hits,
            cache_misses=total - hits,
            avg_similarity_score=avg_sim,
            cache_size_bytes=cache_size,
            most_common_queries=common_queries,
            avg_response_time_saved_ms=avg_time_saved
        )

    def print_report(self, time_window_hours: int = 24):
        """Print a human-readable cache performance report."""
        metrics = self.get_metrics(time_window_hours)
        
        hit_rate = (metrics.cache_hits / metrics.total_queries * 100) if metrics.total_queries > 0 else 0
        
        print("\n📊 Cache Performance Report")
        print("=" * 40)
        print(f"Time Window: Last {time_window_hours} hours")
        print(f"Total Queries: {metrics.total_queries}")
        print(f"Cache Hit Rate: {hit_rate:.1f}%")
        print(f"Average Similarity Score: {metrics.avg_similarity_score:.3f}")
        print(f"Average Time Saved: {metrics.avg_response_time_saved_ms:.0f}ms")
        print(f"Cache Size: {metrics.cache_size_bytes / 1024 / 1024:.1f}MB")
        
        print("\nMost Common Queries:")
        for query, count in metrics.most_common_queries:
            print(f"- '{query}' ({count} times)") 