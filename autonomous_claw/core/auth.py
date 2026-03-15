import os
import requests
from autonomous_claw.core.config import config

_cached_token = None
_token_expiry = 0

def get_oauth_token() -> str:
    """
    Fetches an OAuth Access Token.
    1. Tries standard OAuth2 Client Credentials flow if configured.
    2. Falls back to Google Application Default Credentials (ADC) if google-auth is installed.
    """
    global _cached_token, _token_expiry
    import time
    
    if _cached_token and time.time() < _token_expiry:
        return _cached_token

    token_url = config.oauth_token_url
    client_id = config.oauth_client_id
    client_secret = config.oauth_client_secret

    if token_url and client_id and client_secret:
        try:
            response = requests.post(token_url, data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            }, timeout=10)
            response.raise_for_status()
            data = response.json()
            _cached_token = data.get("access_token", "")
            _token_expiry = time.time() + data.get("expires_in", 3600) - 60
            return _cached_token
        except Exception as e:
            print(f"Error fetching generic OAuth token: {e}")
            return ""

    # Support for Google Vertex / Gemini via Google Auth
    try:
        import google.auth
        import google.auth.transport.requests
        credentials, project = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        _cached_token = credentials.token
        # Cache for a short time to avoid rapid refreshes
        _token_expiry = time.time() + 1800 
        return _cached_token
    except ImportError:
        pass
    except Exception as e:
        pass
        
    return ""
