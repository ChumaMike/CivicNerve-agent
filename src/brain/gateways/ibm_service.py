import os
import time
import requests
import json
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configuration (Load from Env Vars for Security)
IBM_CLOUD_URL = os.getenv("IBM_CLOUD_URL", "https://us-south.ml.cloud.ibm.com")
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")

# IAM token cache — tokens are valid for 3600s; refresh 60s before expiry
_token_cache = {"token": None, "expires_at": 0}


def get_access_token() -> Optional[str]:
    """Exchanges API Key for a Bearer Token with caching to avoid per-request auth overhead."""
    if not API_KEY:
        return None

    # Return cached token if still valid
    if _token_cache["token"] and time.time() < _token_cache["expires_at"] - 60:
        return _token_cache["token"]

    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)
        if response.status_code == 200:
            payload = response.json()
            _token_cache["token"] = payload.get("access_token")
            _token_cache["expires_at"] = time.time() + payload.get("expires_in", 3600)
            return _token_cache["token"]
        print(f"❌ IBM Auth Failed: {response.text}")
        return None
    except Exception as e:
        print(f"❌ Connection Error during IBM auth: {e}")
        return None


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type(requests.exceptions.RequestException),
    reraise=True
)
def _call_ibm_api(url: str, headers: dict, payload: dict) -> requests.Response:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response


def query_granite_model(prompt_text: str) -> Optional[str]:
    """Sends the prompt to IBM Granite with token caching and retry logic."""
    token = get_access_token()
    if not token or not PROJECT_ID:
        return None

    url = f"{IBM_CLOUD_URL}/ml/v1/text/generation?version=2023-05-29"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model_id": "ibm/granite-3-8b-instruct",
        "input": (
            f"You are a strict municipal AI. Extract data from this text into valid JSON only.\n\n"
            f"Text: {prompt_text}\n\nJSON Output:"
        ),
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 400,
            "min_new_tokens": 10,
            "repetition_penalty": 1.1
        },
        "project_id": PROJECT_ID
    }

    try:
        response = _call_ibm_api(url, headers, payload)
        result = response.json()
        return result["results"][0]["generated_text"]
    except requests.exceptions.RequestException as e:
        print(f"⚠️ IBM Granite API failed after retries: {e}")
        return None
    except Exception as e:
        print(f"⚠️ IBM Granite unexpected error: {e}")
        return None
