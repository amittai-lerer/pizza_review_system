# 🍕 Pizza Review RAG — Intelligent Pizza Discovery with LLMs & Vector Search

This project is a modular, production-grade Retrieval-Augmented Generation (RAG) system for intelligent pizza recommendations, combining Large Language Models (LLMs) with semantic vector search. It features a FastAPI backend and a Streamlit frontend, leveraging LangChain for orchestration, ChromaDB for vector retrieval, and Hugging Face embeddings for similarity scoring. The system includes components for query rewriting, city extraction, and context-aware answer generation using local (Ollama) or cloud-based (Together AI) models. Built to demonstrate scalable and maintainable AI engineering practices, the architecture provides a clear blueprint for real-world applications of LLMs in structured information retrieval.


---

## 📊 Project Highlights

* 🔄 **LLM Switching**: Use either a **local model** (`llama3` via Ollama) or a **cloud model** (Together AI)
* 🧠 **Prompt Rewriting**: Refines user queries to improve search and answer quality
* 🖜️ **City Extraction**: Converts slang or abbreviations like `TLV` → `Tel Aviv`
* 🔍 **Vector Search**: Uses ChromaDB with Hugging Face embeddings for fast semantic retrieval
* 🖥️ **Modern UI**: Streamlit frontend with FastAPI backend
* 🐃 **Clean Backend API**: Modular FastAPI server for scalability and production-readiness
* 🐳 **Docker Support**: Easy to containerize for deployment or portability

---

## 🔎 Technologies Used

| Layer      | Tool / Lib                                                                      |
| ---------- | ------------------------------------------------------------------------------- |
| LLM        | [Ollama](https://ollama.com), [Together AI](https://www.together.ai), LangChain |
| Vector DB  | [ChromaDB](https://www.trychroma.com)                                           |
| Embeddings | [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)         |
| Backend    | [FastAPI](https://fastapi.tiangolo.com)                                         |
| Frontend   | [Streamlit](https://streamlit.io)                                               |
| Logging    | Python built-in logging module                                                  |
| Container  | Docker, Docker Compose                                                          |

---

## 📁 Folder Structure

```bash
pizza_review_system/
├── app.py              # Streamlit interface
├── main.py             # FastAPI backend entrypoint
├── backend/
│   ├── api.py          # FastAPI route handler
│   ├── core.py         # Prompt logic, LLM calls, city extraction
│   ├── vector.py       # Vector store loading & query interface
│   └── logger_config.py# Logging config
├── data/               # Contains review CSV file
├── logs/               # Output logs (app.log, vector.log, etc.)
├── .streamlit/         # Streamlit config + secrets.toml (ignored by Git)
├── Dockerfile          # Container build instructions
├── docker-compose.yml  # Optional container orchestrator
├── requirements.txt    # Python dependencies
└── README.md           # You're here.
```

---

## 💪 Key Features

### ✅ LLM Query Rewriting

* Rewrites vague or casual input into semantically structured prompts
* Example: `pizza in JLM?` → `I had great pizza in Jerusalem.`

### ✅ Semantic Retrieval

* Filters reviews by city and meaning
* Uses sentence embeddings and ChromaDB for similarity search

### ✅ Modular RAG Backend (FastAPI)

* `/ask-pizza` endpoint receives questions and returns structured JSON
* Can be consumed by any frontend (Streamlit, React, mobile app, etc.)

### ✅ Frontend (Streamlit)

* Allows toggling between LLMs
* Displays generated answers and source reviews with metadata

### ✅ Logging

* Tracks LLM calls, user queries, vector DB usage
* Logs to file and terminal

---

## 🚀 Setup Instructions

### 1. Clone & Install

```bash
git clone https://github.com/amittai-lerer/pizza_review_system.git
cd pizza_review_system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 🔐 Add Secrets for Cloud Model (Optional)

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

```toml
TOGETHER_API_KEY = "your-together-api-key"
```

### 3. 🧠 Run Ollama Model (Optional)

```bash
ollama pull llama3
ollama run llama3
```

### 4. 🚀 Launch Backend API

```bash
python main.py
```

This runs the FastAPI server on: [http://localhost:8000](http://localhost:8000)

### 5. 🚀 Launch Frontend App

```bash
streamlit run app.py
```

Streamlit will run at: [http://localhost:8501](http://localhost:8501)

---

## 🕵️‍♂️ Sample Queries

```text
Best pizza in TLV?
Spiciest toppings in Haifa?
Authentic Neapolitan pizza in JLM?
Where to find gluten-free pizza in Holon?
Top-rated places for pizza crust?
```

---

## 🐳 Docker Support (Optional)

```bash
docker build -t pizza-review .
docker run -p 8501:8501 pizza-review
```

Or with Docker Compose:

```bash
docker-compose up
```

---

## 🔒 License

MIT License — Freely usable for educational, demo, or portfolio purposes.
