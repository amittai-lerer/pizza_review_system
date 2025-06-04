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

A sophisticated Natural Language Processing system that leverages Large Language Models (LLMs), vector embeddings, and semantic search to provide intelligent analysis of Israeli pizza restaurant reviews. Built with modern software engineering practices and a clean, production-ready architecture using Docker Compose.

---

## 📊 Project Highlights

- Semantic search across user reviews of Israeli pizzerias.
- Intelligent Q&A using LangChain + Ollama (`llama3`) + ChromaDB.
- Modular Python architecture with comprehensive logging.
- Fully containerized with Docker Compose for easy setup and consistent environments.
- Entirely local LLM inference ensuring privacy and speed.

---

## 🔎 Technologies Used

| Layer       | Tool / Lib                        |
|-------------|-----------------------------------|
| LLM         | [Ollama](https://ollama.com) (`llama3` model) + LangChain |
| Vector DB   | ChromaDB                          |
| UI          | Streamlit                         |
| Embeddings  | BAAI/bge-small-en-v1.5 (Hugging Face) |
| Logging     | Python `logging` module (file & console output) |
| Packaging   | Docker & Docker Compose           |

---

## 📊 Folder Structure

```
pizza_review_system/
├── app.py              # Streamlit User Interface
├── core.py             # Core logic: prompt engineering, LLM interaction, city extraction
├── vector.py           # Vector store management (ChromaDB loading & querying)
├── logger_config.py    # Shared logging configuration utility
├── data/               # Contains the source CSV review dataset
├── logs/               # Directory for output logs (e.g., app.log, core.log)
├── Dockerfile          # Instructions to build the Streamlit application container
├── docker-compose.yml  # Defines and orchestrates the multi-container application (Streamlit app + Ollama)
├── requirements.txt    # Python dependencies for the Streamlit application
├── .dockerignore       # Specifies intentionally untracked files for Docker build context
└── README.md           # This file: project overview and instructions
```

---

## 💪 Features

### ✅ Smart LLM Prompting & Interaction
- Dynamically rewrites user questions into effective semantic search queries.
- Accurately extracts and normalizes city names (e.g., "TLV" is understood as "Tel Aviv").
- Utilizes LangChain for robust and structured communication with the LLM.

### ✅ Vector-Based Retrieval with ChromaDB
- Achieves fast and relevant semantic search over reviews using vector embeddings.
- Supports filtering of search results by city metadata for targeted information.
- Employs Hugging Face embeddings (`BAAI/bge-small-en-v1.5`) for semantic similarity.

### ✅ Interactive UI with Streamlit
- Provides a clean, single-input interface for user queries.
- Displays LLM-generated answers clearly.
- Allows users to expand results to see the specific reviews used for context.

### ✅ Comprehensive Logging & Debugging
- Outputs logs to both files (e.g., `logs/app.log`, `logs/core.log`) and the console.
- Offers a detailed trace of the entire process: query rewrite, city filtering, vector search, and LLM calls.

---

## 🚀 Setup and Run with Docker Compose (Recommended)

This is the easiest and most reliable way to run the application, as it manages both the Streamlit app and the Ollama LLM service in isolated, consistent environments.

**Prerequisites:**
- Docker Desktop (or Docker Engine + Docker Compose CLI) installed and running.

**Instructions:**

1.  **Clone the Project:**
    ```bash
    git clone https://github.com/amittai-lerer/pizza_review_system.git
    cd pizza_review_system
    ```

2.  **Build and Start the Services:**
    This command will build the `pizza-app` image using the `Dockerfile` and pull the official `ollama/ollama` image. It then starts both services in detached mode.
    ```bash
    docker-compose up --build -d
    ```

3.  **Pull the LLM Model into Ollama:**
    After the services are up (especially the `ollama` service), you need to pull the `llama3` model into the Ollama container. This is a one-time setup per model unless the Ollama volume is removed.
    ```bash
    docker-compose exec ollama ollama pull llama3
    ```
    You can check available models inside Ollama with `docker-compose exec ollama ollama list`.

4.  **Access the Streamlit App:**
    Open your web browser and navigate to:
    [http://localhost:7860](http://localhost:7860)

**To Stop the Services:**
```bash
docker-compose down
```

---

## 🧑‍💻 Local Development Setup (Alternative)

If you prefer to run the Streamlit app directly on your host machine for development (e.g., for faster iteration on UI changes), you can follow these steps. You'll still need Ollama running (either locally or via Docker).

1.  **Clone the Project** (if not already done):
    ```bash
    git clone https://github.com/amittai-lerer/pizza_review_system.git
    cd pizza_review_system
    ```

2.  **Set Up Python Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Ensure Ollama is Running and `llama3` is Available:**
    You can run Ollama directly on your host machine (see [Ollama download](https://ollama.com/download)) or keep the Ollama service from `docker-compose.yml` running (`docker-compose up -d ollama`).
    Make sure the `llama3` model is pulled:
    ```bash
    ollama pull llama3 # If Ollama is running locally on host
    # or docker-compose exec ollama ollama pull llama3 # If using Ollama via Docker Compose
    ```

4.  **Run the Streamlit App Locally:**
    ```bash
    streamlit run app.py
    ```
    The app will typically be available at `http://localhost:8501` (Streamlit's default port when run this way).

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

