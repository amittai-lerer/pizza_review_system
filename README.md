---
title: Pizza Review RAG
emoji: 🍕
colorFrom: red
colorTo: yellow
sdk: streamlit
app_file: app.py
pinned: false
---


# Pizza Review Analysis System

An advanced question-answering system for exploring pizza restaurant reviews using LangChain, ChromaDB, and local LLM inference through Ollama.

## Features

- Semantic search powered by BAAI/bge-small-en-v1.5 embeddings
- Intelligent query rewriting for better search results
- City-aware filtering with smart city name normalization
- Natural language question answering using Llama 3.2
- Beautiful Streamlit dashboard with:
  - Form-based query submission
  - Styled answer display
  - Expandable review details
  - Emoji-enhanced UI elements
- Comprehensive review metadata integration (ratings, dates, categories)
- Persistent vector storage for fast retrieval

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed with llama3.2
- Sufficient disk space for the vector store

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd pizza_review_system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Ensure you have the required Ollama model:
```bash
ollama pull llama3.2
```

## Data Structure

The system uses a structured CSV format (`data/combined_reviews.csv`) with the following columns:
- Title: Restaurant name
- Review: Full review text
- Rating: Numerical rating (float)
- Date: Review date
- City: Location city
- State: Location state
- Categories: Business categories/tags

## Usage

1. First run will initialize the vector store:
```bash
python vector.py
```

2. Start the interactive dashboard:
```bash
streamlit run app.py
```

The dashboard provides:
- Clean, form-based interface
- Real-time query processing
- Beautifully formatted answers
- Expandable review details with metadata
- Emoji-enhanced visualization

Example questions:
- "What are the best pizza places in Tel Aviv?"
- "Where can I find authentic New York style pizza?"
- "Tell me about kosher pizza options in Jerusalem"

## Project Structure

- `app.py`: Streamlit interface featuring:
  - Form-based query input
  - Styled answer display
  - Expandable review details
  - Enhanced visual elements
  
- `core.py`: Core Q&A system implementing:
  - Query preprocessing
  - Review retrieval and formatting
  - Answer generation
  
- `vector.py`: Vector store management:
  - Document processing and embedding
  - ChromaDB integration
  - City-filtered retrieval logic

- `data/`: Contains review datasets
  - `combined_reviews.csv`: Primary review data
  
- `chroma_langchain_db/`: Vector store directory (auto-generated)

## Technical Implementation

### Vector Store (vector.py)
- Uses BAAI/bge-small-en-v1.5 for high-quality embeddings
- ChromaDB backend for efficient vector storage
- Metadata-aware retrieval with city filtering
- Automatic document processing from CSV

### Q&A System (core.py)
- Two-stage LLM pipeline:
  1. Query preprocessing:
     - City name normalization
     - Query rewriting for better semantic matching
  2. Answer generation:
     - Context-aware response formulation
     - Location-specific recommendations
     - Natural, conversational tone

### Dashboard (app.py)
- Modern Streamlit interface with:
  - Form-based input handling
  - Real-time query processing
  - Styled answer display
  - Expandable review sections
  - Enhanced visual elements

## Notes

- The vector store is persisted in `chroma_langchain_db/` (gitignored)
- First run will take longer due to vector store initialization
- System supports incremental data updates
- Responses are generated locally using Ollama

## Troubleshooting

- If search results are unexpected, check:
  1. City spelling and normalization
  2. Vector store initialization
  3. Review data formatting
  
- For performance issues:
  1. Verify Ollama installation
  2. Check system resources
  3. Monitor vector store size 