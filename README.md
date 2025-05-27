---
title: Pizza Review RAG
emoji: 🍕
colorFrom: red
colorTo: yellow
sdk: streamlit
app_file: app.py
pinned: false
---

# 🍕 Pizza Review Analysis System

An intelligent question-answering system for exploring Israeli pizza restaurant reviews, powered by LangChain, ChromaDB, and dual LLM support (local Ollama and cloud Hugging Face).

## ✨ Features

- **Smart Search**
  - Semantic search with BAAI/bge-small-en-v1.5 embeddings
  - Intelligent query rewriting and normalization
  - City-aware filtering with name standardization

- **Dual LLM Architecture**
  - Primary: Local Llama 3.2 via Ollama
  - Fallback: Cloud-based LLaMA via Hugging Face
  - Automatic failover mechanism

- **Modern Interface**
  - Clean Streamlit dashboard
  - Real-time response display
  - Expandable review details
  - Environment-aware configuration

- **Robust Infrastructure**
  - Comprehensive logging system
  - Persistent vector storage
  - Docker support with auto-detection
  - Centralized configuration

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- Python 3.8+
- Ollama (with llama3.2 model)
- Hugging Face API token
- 2GB+ free disk space

# Optional
- Docker & Docker Compose (for containerized deployment)
```

### Installation

1. Clone and setup:
```bash
git clone <your-repo-url>
cd pizza_review_system
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
# Install Ollama model
ollama pull llama3.2

# Create .streamlit/secrets.toml
mkdir -p .streamlit
echo "HUGGINGFACE_API_TOKEN = 'your-token-here'" > .streamlit/secrets.toml
```

3. Run the app:
```bash
streamlit run app.py
```

### Docker Deployment

```bash
docker-compose up --build
```

## 🏗️ Architecture

### Core Components

```
pizza_review_system/
├── app.py              # Streamlit interface
├── core.py            # Query processing & answer generation
├── vector.py          # Vector store & retrieval
├── llm_loader.py      # LLM integration & fallback
├── logger_config.py   # Centralized logging
├── data/              # Review datasets
├── logs/              # Application logs
└── docker/            # Container configuration
```

### Key Modules

1. **Query Processing** (`core.py`)
   - Question analysis
   - City extraction
   - Query rewriting
   - Answer generation

2. **Vector Store** (`vector.py`)
   - Document embedding
   - Semantic search
   - City-based filtering
   - Metadata management

3. **LLM Integration** (`llm_loader.py`)
   - Local model integration
   - Cloud fallback mechanism
   - Error handling
   - Response processing

4. **Logging System** (`logger_config.py`)
   - Structured logging
   - File & console output
   - Debug/Info/Warning levels
   - Emoji-enhanced readability

## 📝 Usage Examples

```python
# Basic question
"What are the best pizza places in Tel Aviv?"

# Specific criteria
"Where can I find authentic New York style pizza in Jerusalem?"

# General inquiry
"Tell me about kosher pizza options near the beach"
```

## 📊 Logging

The system maintains detailed logs in two locations:
- `logs/app.log`: General application events
- `logs/llm.log`: LLM interactions and responses

Log levels:
- `INFO`: Normal operations
- `DEBUG`: Detailed processing info
- `WARNING`: Non-critical issues
- `ERROR`: Critical problems

## 🔧 Troubleshooting

### LLM Issues
1. Local Model (Ollama)
   - Verify Ollama is running: `ollama list`
   - Check model installation: `ollama pull llama3.2`
   - Monitor logs: `logs/llm.log`

2. Cloud Fallback
   - Verify API token in `.streamlit/secrets.toml`
   - Check network connectivity
   - Monitor rate limits

### Vector Store
1. Initialization
   - Ensure sufficient disk space
   - Check file permissions
   - Verify data file format

2. Performance
   - Monitor memory usage
   - Check index size
   - Verify embedding quality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details 