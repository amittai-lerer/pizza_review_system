"""
LLM Loader
==========

Handles local LLM requests using Ollama.
Simple, function-based design for consistency across codebase.
"""

import os
import requests
from logger_config import setup_logger

# --- Logger ---
logger = setup_logger(name="llm", log_file="logs/llm.log")

# --- Config ---
LOCAL_MODEL = "llama3:latest"
LOCAL_PORT = 11434
LOCAL_HOST = "ollama" if os.path.exists("/.dockerenv") else "localhost"
TEMPERATURE = 0.7
MAX_TOKENS = 256

def is_running_in_docker() -> bool:
    """Check if the application is running inside Docker."""
    return os.path.exists('/.dockerenv')

def get_local_response(prompt: str) -> str:
    """Send request to local LLM (Ollama)."""
    url = f"http://{LOCAL_HOST}:{LOCAL_PORT}/api/generate"
    payload = {
        "model": LOCAL_MODEL,
        "prompt": prompt,
        "options": {
            "temperature": TEMPERATURE,
            "num_predict": MAX_TOKENS
        },
        "stream": False
    }

    logger.info(f"💻 Requesting from local model '{LOCAL_MODEL}' at {LOCAL_HOST}:{LOCAL_PORT}")
    logger.debug(f"📤 Prompt to local: {prompt}")

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()["response"].strip()
        logger.debug(f"📥 Local response: {result}")
        return result
    except requests.exceptions.ConnectionError:
        error_msg = f"Could not connect to Ollama at {LOCAL_HOST}:{LOCAL_PORT}. Make sure Ollama is running and the model '{LOCAL_MODEL}' is installed."
        logger.error(error_msg)
        raise ConnectionError(error_msg)
    except Exception as e:
        error_msg = f"Error getting response from local LLM: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)

def get_llm_response(prompt: str, mode: str = "local") -> str:
    """
    Get response from local LLM.

    Args:
        prompt: The input prompt string.
        mode: Only 'local' is supported

    Returns:
        The response from the local LLM as a string.
    """
    if mode != "local":
        logger.warning(f"Mode '{mode}' not supported. Using local mode.")
    
    return get_local_response(prompt)
