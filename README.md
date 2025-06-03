---
title: Pizza Review RAG
emoji: 🍕
colorFrom: red
colorTo: yellow
sdk: streamlit
app_file: app.py
pinned: false
---

# 🍕 Advanced NLP-Powered Pizza Review Analysis System

A sophisticated Natural Language Processing system that leverages Large Language Models (LLMs), vector embeddings, and semantic search to provide intelligent analysis of Israeli pizza restaurant reviews. Built with modern software engineering practices and a clean, production-ready architecture.

---

## 📊 Project Highlights

- Semantic search across user reviews of Israeli pizzerias
- Intelligent Q&A using LangChain + Ollama + ChromaDB
- Modular architecture with full logging and docker support
- Fully local LLM inference using `llama3` via Ollama

---

## 🔎 Technologies Used

| Layer       | Tool / Lib                        |
|-------------|-----------------------------------|
| LLM         | [Ollama](https://ollama.com) + LangChain |
| Vector DB   | ChromaDB                          |
| UI          | Streamlit                         |
| Embeddings  | BAAI/bge-small-en-v1.5 (HF)       |
| Logging     | Python logger w/ file output      |
| Packaging   | Docker, Docker Compose            |

---

## 📊 Folder Structure

```
pizza_review_system/
├── app.py              # Streamlit interface
├── core.py             # Prompt logic, LLM calls, city extraction
├── vector.py           # Vector store loading & query interface
├── logger_config.py    # Logging config shared across modules
├── data/               # Contains review CSV file
├── logs/               # Output logs (app.log, vector.log, etc.)
├── Dockerfile          # Container build instructions
├── docker-compose.yml  # Optional container orchestrator
├── requirements.txt    # Python dependencies
├── README.md           # You're here.
```

---

## 💪 Features

### ✅ Smart LLM Prompting
- Rewrites user questions into semantic search queries
- Extracts & normalizes city names ("TLV" → "Tel Aviv")
- Ensures consistent prompt format for reliable LLM use

### ✅ Vector-Based Retrieval
- Fast semantic search via ChromaDB
- Filters by city metadata
- Uses Hugging Face embeddings for similarity

### ✅ Clean UI in Streamlit
- Single input for user queries
- Expandable review results
- Annotated answers with context

### ✅ Logging & Debugging
- File + terminal logging (e.g., `logs/app.log`)
- Detailed trace of rewrite, filter, query, and LLM call

---

## 🚀 Setup Instructions

```bash
# Clone the project
git clone https://github.com/amittai-lerer/pizza_review_system.git
cd pizza_review_system

# Set up environment
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# Install dependencies
pip install -r requirements.txt
```

### 🫠 Run Ollama LLM Locally
```bash
# Make sure you have Ollama installed (https://ollama.com/download)
ollama pull llama3
ollama run llama3
```

### 🌐 Run Streamlit App
```bash
streamlit run app.py
```

Open the browser at [http://localhost:8501](http://localhost:8501)

---

## 💡 Sample Queries
```text
Best pizza in TLV?
What are top Neapolitan pizza places?
Which pizzeria in Jerusalem has spicy toppings?
Who has the best pizza crust?
```

---

## 🌟 License

This project is licensed under the MIT License.









--------------




---
title: Pizza Review RAG
emoji: 🍕
colorFrom: red
colorTo: yellow
sdk: streamlit
app_file: app.py
pinned: false
---

# 🍕 Pizza Review RAG – AI-Powered Pizza Discovery in Israel

This is a full-stack, AI-driven system that allows users to ask natural language questions about pizza in Israeli cities, powered by local LLMs, vector search, and intelligent prompt rewriting.

Built with production-ready architecture, clear modular design, and fully local inference using [Ollama](https://ollama.com), this project demonstrates advanced use of LangChain, Streamlit, and ChromaDB.

---

## 🚀 Demo
![App Screenshot](docs/screenshot.png) <!-- Add your own image or gif here -->

---

## 🌐 Tech Stack Overview

| Layer     | Tools / Technologies                     |
|-----------|------------------------------------------|
| LLM       | `llama3.2` via Ollama                    |
| Prompting | LangChain + `ChatPromptTemplate`         |
| Vector DB | ChromaDB + HuggingFace Embeddings        |
| Backend   | Python + modular `core.py`, `vector.py`  |
| Frontend  | Streamlit                                |
| Logging   | Custom file+console logger               |

---

## 📊 Architecture

```
pizza_review_system/
├── app.py              # Streamlit interface
├── core.py             # Rewriting + LLM answering
├── vector.py           # Embedding + retrieval logic
├── logger_config.py    # Shared logging utility
├── data/               # Source CSV reviews
├── logs/               # app.log, vector.log, etc.
├── Dockerfile          # App container
├── docker-compose.yml  # LLM + App stack
├── requirements.txt    # All dependencies
└── README.md           # You're here
```

### Core Components

- **`core.py`**
  - Extracts cities from natural language queries (e.g., "TLV" → "Tel Aviv")
  - Rewrites vague questions into review-style prompts
  - Uses LangChain chains + `OllamaLLM` locally

- **`vector.py`**
  - Loads reviews from CSV into ChromaDB
  - Embeds using `BAAI/bge-small-en-v1.5`
  - Supports filtering by `city` metadata

- **`app.py`**
  - Single input form via Streamlit
  - Handles query, result display, and LLM output
  - Expands results, shows raw reviews used

---

## 🛠 Setup Instructions

### 1. Clone and Install
```bash
git clone <your-repo-url>
cd pizza_review_system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Start Ollama and Pull the Model
```bash
ollama pull llama3
ollama run llama3
```

### 3. Start the App
```bash
streamlit run app.py
```

Then visit: [http://localhost:8501](http://localhost:8501)

---

## 🔎 Example Queries

```text
Best pizza crust in TLV?
Authentic Neapolitan pizza in JLM?
Who serves the spiciest toppings in Haifa?
Where can I get wood-fired pizza?
```

---

## 🚧 Engineering Highlights

- ✅ Rewrites natural language to search-friendly prompts
- ✅ Extracts + normalizes cities (e.g., TLV → Tel Aviv)
- ✅ Uses vector similarity search for smart retrieval
- ✅ Entirely local inference via Ollama
- ✅ Logs all actions to `logs/`
- ✅ Modular, extendable architecture


---

## 🔒 License

MIT License. See [LICENSE](LICENSE) for full terms.

---

