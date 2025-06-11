# Technology Choices: ChromaDB vs SQLite

This project uses two storage systems, each optimized for a different purpose.

---

## 🧠 ChromaDB (for Reviews)

Used to store vector embeddings of pizza reviews for semantic search.

- 🔍 Fast **approximate similarity search** using an index (HNSW)
- ⚡ Scales to thousands+ of vectors efficiently
- 🛠️ Integrates easily with LangChain and supports metadata filtering

**Why an Index?**  
Chroma uses graph-based indexing (HNSW) to avoid scanning every vector — results in **millisecond search even with large datasets**.

---

## ⚡ SQLite (for LLM Caching)

Used to cache recent Q&A pairs from LLM calls.

- 💾 Lightweight, file-based — no server required
- ✅ Ideal for small, local caches (<1,000 entries)
- 🧹 Includes TTL expiry and hit tracking

**Why Linear Search?**  
Cosine similarity is computed manually for each cached entry. Works well at small scale, but not ideal for large datasets.

---


##########################################################################################################################################

This project supports two LLM execution modes, each optimized for different environments and use cases.

🧠 Local LLM (Ollama)
Used to run inference locally using the llama3 model.

✅ Fast, offline, and free of API costs
🧪 Ideal for development, testing, and rapid iteration
🔐 Fully private — no external network calls required

Why Local?
Local inference enables fast feedback loops, cost efficiency, and privacy. Best suited for early-stage development or offline work.

---

☁️ Cloud LLM (Together AI)
Used to access advanced hosted models like Llama-3.3-70B-Instruct-Turbo-Free.

🧠 Provides superior reasoning, coherence, and natural language quality
🚀 Suitable for production environments, interviews, and high-stakes output
🌐 Requires API access and a stable internet connection

Why Cloud?
Cloud models offer stronger performance at the cost of external dependencies and latency. Useful when accuracy and fluency are critical.



