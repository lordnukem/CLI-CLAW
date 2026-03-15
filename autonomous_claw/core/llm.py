import requests
import json
from autonomous_claw.core.config import config
from autonomous_claw.core.auth import get_oauth_token

def generate_response(system_prompt: str, user_prompt: str, model: str | None = None) -> str:
    """
    Sends a request to an OpenAI-compatible /v1/chat/completions endpoint.
    Prioritizes OAuth token generation if enabled, before falling back to static API keys.
    """
    chosen_model = model or config.default_model
    url = f"{config.api_base.rstrip('/')}/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    # Handle Authentication (OAuth Default, fallback to API Key)
    token = None
    if config.use_oauth:
        token = get_oauth_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
    if not token:
        api_key = config.api_key
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        else:
            return f"[Simulated Output for {chosen_model}]: Authentication Failed. No OAuth token or API Key resolved."

    
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
