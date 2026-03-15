import requests
import json
from autonomous_claw.core.config import config

def generate_response(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """
    Sends a request to an OpenAI-compatible /v1/chat/completions endpoint.
    Doesn't require heavy dependencies to run.
    """
    chosen_model = model or config.default_model
    api_key = config.api_key
    url = f"{config.api_base.rstrip('/')}/chat/completions"

    if not api_key:
        return f"[Simulated Output for {chosen_model}]: I received your prompt but no API key was configured."

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": chosen_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Fallback or error reporting
        return f"Error connecting to LLM provider ({url}): {e}"
