# Pizza Review Analysis System

A question-answering system that analyzes pizza restaurant reviews using LangChain and Ollama.

## Features

- City-aware search with case-insensitive matching
- Semantic search for pizza reviews
- Natural language question answering
- LLM-powered city name normalization (e.g., "NYC" → "New York")

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed with the following models:
  - llama3.2 (for question answering)
  - mxbai-embed-large (for embeddings)

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

4. Ensure you have the required Ollama models:
```bash
ollama pull llama3.2
ollama pull mxbai-embed-large
```

## Data Structure

The system expects review data in CSV format with the following columns:
- Title: Restaurant name
- Review: Review text
- Rating: Numerical rating
- Date: Review date
- City: City name (case-insensitive matching)
- State: State code
- Categories: Business categories

## Usage

Run the main script:
```bash
python main.py
```

The system will:
1. Load and process reviews from the data directory
2. Create a vector store for semantic search
3. Start an interactive Q&A session where you can ask questions like:
   - "What are the best pizza places in New York?"
   - "Tell me about pizza restaurants in Chicago"
   - "What do people say about NYC pizza?"

## Project Structure

- `main.py`: Main Q&A system with LLM-powered city normalization
- `vector.py`: Vector store implementation with case-insensitive city filtering
- `data/`: Directory containing review datasets
- `requirements.txt`: Project dependencies

## Technical Details

- Uses ChromaDB for vector storage
- Case-insensitive city matching for reliable filtering
- LLM city name normalization (e.g., "NYC", "Manhattan" → "New York")
- Top-5 most relevant results per query

## Notes

- The vector store (`chroma_langchain_db/`) is gitignored and will be recreated on first run
- City names are stored and matched case-insensitively for consistent results
- Virtual environment (`venv/`) is gitignored

## Additional Notes

- CSV data file should be added manually after cloning 