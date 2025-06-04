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

2. 🔐 Add Secrets for Cloud Model (Optional)

To use the Together AI model, create a file at:

.streamlit/secrets.toml

Add your API key:

TOGETHER_API_KEY = "your-together-api-key"

⚠️ This file is already excluded from version control via .gitignore.

3. 🧠 Run Ollama Locally (Optional)

If you prefer local LLM inference:

ollama pull llama3
ollama run llama3

4. 🚀 Launch the App

streamlit run app.py

Open your browser to: http://localhost:8501

💬 Example Queries

Best pizza in TLV?
Spiciest toppings in Haifa?
Authentic Neapolitan pizza in JLM?
Where to find gluten-free pizza in Holon?
Top-rated places for pizza crust?

🧪 Cloud Model Integration (Optional)

If using Together AI:

Ensure TOGETHER_API_KEY is set in .streamlit/secrets.toml

The app will automatically switch to Together AI when enabled

Default model:meta-llama/Llama-3.3-70B-Instruct-Turbo-Free

🐳 Docker Support (Optional)

To build and run the app in a container:

docker build -t pizza-review .
docker run -p 8501:8501 pizza-review

Or use Docker Compose:

docker-compose up

📜 License

MIT License — freely usable for educational or portfolio purposes.

