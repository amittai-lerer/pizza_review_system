# Pizza Review Analysis System

A question-answering system that analyzes pizza restaurant reviews using LangChain and Ollama.

## Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.ai/) installed with the following models:
  - llama2
  - mxbai-embed-large

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
ollama pull llama2
ollama pull mxbai-embed-large
```

5. Place your reviews CSV file in the project root:
- File name: `realistic_restaurant_reviews.csv`
- Required columns: Title, Review, Rating, Date

## Usage

Run the main script:
```bash
python main.py
```

The system will:
1. Load and process reviews on first run
2. Create a vector store for semantic search
3. Start an interactive Q&A session

## Project Structure

- `main.py`: Main Q&A system implementation
- `vector.py`: Vector store and embedding implementation
- `requirements.txt`: Project dependencies
- `realistic_restaurant_reviews.csv`: Review data (not included in repo)

## Notes

- The vector store (`chroma_langchain_db/`) is gitignored and will be recreated on first run
- Virtual environment (`venv/`) is gitignored
- CSV data file should be added manually after cloning 