"""
LLM Loader
==========

Handles local/cloud LLM requests with fallback logic.
Simple, function-based design for consistency across codebase.
"""

import os
import requests
import streamlit as st
from logger_config import setup_logger

# --- Logger ---
logger = setup_logger(name="llm", log_file="logs/llm.log")

# --- Config ---
LOCAL_MODEL = "llama3.2"
LOCAL_PORT = 11434
LOCAL_HOST = "ollama" if os.path.exists("/.dockerenv") else "localhost"
CLOUD_MODEL = "meta-llama/Meta-Llama-3-8B-Instruct"
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

    response = requests.post(url, json=payload)
    response.raise_for_status()

    result = response.json()["response"].strip()
    logger.debug(f"📥 Local response: {result}")
    return result

def get_cloud_response(prompt: str) -> str:
    """Send request to Hugging Face cloud model."""
    url = f"https://api-inference.huggingface.co/models/{CLOUD_MODEL}"
    headers = {
        "Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": TEMPERATURE,
            "max_new_tokens": MAX_TOKENS
        }
    }

    logger.info(f"☁️ Requesting from Hugging Face model '{CLOUD_MODEL}'")
    logger.debug(f"📤 Prompt to cloud: {prompt}")

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()[0]["generated_text"].strip()
    logger.debug(f"📥 Cloud response: {result}")
    return result

def get_llm_response(prompt: str, mode: str = "auto") -> str:
    """
    Unified LLM response function with optional mode.

    Args:
        prompt: The input prompt string.
        mode: 'local', 'cloud', or 'auto' (default: auto)

    Returns:
        The response from the LLM as a string.
    """
    logger.info(f"🔁 get_llm_response called [mode={mode}]")

    if mode == "cloud":
        return get_cloud_response(prompt)
    
    if mode == "local":
        return get_local_response(prompt)

    # auto mode with fallback
    try:
        return get_local_response(prompt)
    except Exception as e:
        logger.warning(f"⚠️ Local LLM failed: {e}. Falling back to cloud.")
        return get_cloud_response(prompt)
