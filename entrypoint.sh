#!/bin/bash

echo "🚀 Starting Ollama server..."
ollama serve --host=0.0.0.0 &

# Wait a few seconds for the Ollama server to start
sleep 3

echo "🎯 Launching Streamlit app..."
exec streamlit run app.py --server.port=7860 --server.address=0.0.0.0
