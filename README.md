# Pizza Review Analysis System

An advanced question-answering system for exploring pizza restaurant reviews using LangChain, ChromaDB, and local LLM inference through Ollama.

## Features

- Semantic search powered by BAAI/bge-small-en-v1.5 embeddings
- Intelligent query rewriting for better search results
- City-aware filtering with smart city name normalization
- Natural language question answering using Llama 3.2
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

2. Start the interactive Q&A system:
```bash
python main.py
```

Example questions:
- "What are the best pizza places in Tel Aviv?"
- "Where can I find authentic New York style pizza?"
- "Tell me about kosher pizza options in Jerusalem"

## Project Structure

- `main.py`: Core Q&A system implementing:
  - Query preprocessing and city normalization
  - Review retrieval and context formatting
  - Natural language answer generation
  
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

### Q&A System (main.py)
- Two-stage LLM pipeline:
  1. Query preprocessing:
     - City name normalization
     - Query rewriting for better semantic matching
  2. Answer generation:
     - Context-aware response formulation
     - Location-specific recommendations
     - Natural, conversational tone

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