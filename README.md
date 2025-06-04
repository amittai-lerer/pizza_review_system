
---
title: Pizza Review RAG
emoji: 🍕
colorFrom: red
colorTo: yellow
sdk: streamlit
app_file: app.py
pinned: false
---

# 🍕 Pizza Review RAG – AI-Powered Pizza Discovery for Israel

A sophisticated Natural Language Processing (NLP) system that leverages Large Language Models (LLMs), vector embeddings, and semantic search to provide intelligent analysis of Israeli pizza restaurant reviews. Built with production-grade engineering practices and a clean, modular architecture.

---

## 📊 Project Highlights

* 🔄 **LLM Switching**: Use either a **local model** (`llama3` via Ollama) or a **cloud model** (Together AI)
* 🧠 **Prompt Rewriting**: Refines user queries to improve search and answer quality
* 🗜️ **City Extraction**: Converts slang or abbreviations like `TLV` → `Tel Aviv`
* 🔍 **Vector Search**: Uses ChromaDB with Hugging Face embeddings for fast semantic retrieval
* 🖥️ **Modern UI**: Streamlit frontend with logging, query results, and LLM controls
* 🐳 **Docker Support**: Easy to containerize for deployment or portability

---

## 🔎 Technologies Used

| Layer      | Tool / Lib                                                                      |
| ---------- | ------------------------------------------------------------------------------- |
| LLM        | [Ollama](https://ollama.com), [Together AI](https://www.together.ai), LangChain |
| Vector DB  | [ChromaDB](https://www.trychroma.com)                                           |
| Embeddings | [BAAI/bge-small-en-v1.5](https://huggingface.co/BAAI/bge-small-en-v1.5)         |
| UI         | [Streamlit](https://streamlit.io)                                               |
| Logging    | Python built-in logging module                                                  |
| Container  | Docker, Docker Compose                                                          |

---

## 📁 Folder Structure

```
pizza_review_system/
├── app.py              # Streamlit interface
├── core.py             # Prompt logic, LLM calls, city extraction
├── vector.py           # Vector store loading & query interface
├── logger_config.py    # Logging config shared across modules
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

### ✅ Smart LLM Prompting

* Rewrites vague or casual input into semantically structured review prompts
* Example: `pizza in JLM?` → `I had great pizza in Jerusalem.`

### ✅ Semantic Retrieval

* Filters reviews by city and similarity
* Uses BAAI embeddings and ChromaDB for scalable local vector search

### ✅ Flexible LLM Execution

* Use `llama3` locally via Ollama (no API cost)
* Or query Together AI's `Llama-3.3-70B-Instruct-Turbo-Free` in the cloud

### ✅ Rich Logging

* Tracks rewrite steps, LLM calls, parsed results, and user queries
* Logs to both file (`logs/app.log`) and console

## 🚀 Setup Instructions

### 1. Clone & Install

```bash
git clone https://github.com/amittai-lerer/pizza_review_system.git
cd pizza_review_system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 2. 🔐 Add Secrets for Cloud Model (Optional)

To use the Together AI model, create a file:

```bash
mkdir -p .streamlit
nano .streamlit/secrets.toml
```

Add your API key:

```toml
TOGETHER_API_KEY = "your-together-api-key"
```

> ⚠️ This file is excluded from version control by `.gitignore`

---

### 3. 🧠 Run Ollama Locally (Optional)

```bash
ollama pull llama3
ollama run llama3
```

---

### 4. 🚀 Launch the App

```bash
streamlit run app.py
```

Then open your browser at: [http://localhost:8501](http://localhost:8501)

---

## 💬 Example Queries

```text
Best pizza in TLV?
Spiciest toppings in Haifa?
Authentic Neapolitan pizza in JLM?
Where to find gluten-free pizza in Holon?
Top-rated places for pizza crust?
```

---

## 🧪 Cloud Model Integration (Optional)

* Ensure `TOGETHER_API_KEY` is set in `.streamlit/secrets.toml`
* The app automatically switches to Together AI when enabled via the UI toggle
* Default model:

```text
meta-llama/Llama-3.3-70B-Instruct-Turbo-Free
```

---

## 🐳 Docker Support (Optional)

**Build and run the app in a container:**

```bash
docker build -t pizza-review .
docker run -p 8501:8501 pizza-review
```

**Or use Docker Compose:**

```bash
docker-compose up
```

---

## 📜 License

MIT License — Freely usable for educational, demo, or portfolio purposes.

---
