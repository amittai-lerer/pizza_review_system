import os
import requests
import streamlit as st

# 🧠 Detect if running inside a Docker container
def is_running_in_docker() -> bool:
    return os.path.exists('/.dockerenv') or (
        os.path.exists('/proc/self/cgroup') and
        any("docker" in line for line in open("/proc/self/cgroup", "r", errors="ignore"))
    )


# 🔁 CLOUD: Meta LLaMA 3 via Hugging Face
def cloud_LLM(prompt: str, temperature=0.7, max_new_tokens=512) -> str:
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {
        "Authorization": f"Bearer {st.secrets['HUGGINGFACE_API_TOKEN']}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": temperature,
            "max_new_tokens": max_new_tokens
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()[0]["generated_text"].strip()


# 🖥️ LOCAL: LLaMA 3.2 via Ollama HTTP API
def local_LLM(prompt: str, model="llama3.2", temperature=0.7, max_tokens=256) -> str:
    host = "host.docker.internal" if is_running_in_docker() else "localhost"
    url = f"http://{host}:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
        "stream": False
    }

    response = requests.post(url, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"❌ LLaMA local call failed: {response.status_code} - {response.text}")

    return response.json()["response"].strip()


# 🔀 CONTROLLER: Tries local first, fallback to cloud
def get_llm_response(prompt: str, mode="auto") -> str:
    if mode == "cloud":
        return cloud_LLM(prompt)
    elif mode == "local":
        return local_LLM(prompt)

    # AUTO: try local, fallback to cloud
    try:
        return local_LLM(prompt)
    except Exception as e:
        print("⚠️ Local LLM failed. Falling back to cloud:", e)
        return cloud_LLM(prompt)
