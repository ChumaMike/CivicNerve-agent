import os
import requests
import json
from typing import Optional

# Configuration (Load from Env Vars for Security)
IBM_CLOUD_URL = os.getenv("IBM_CLOUD_URL", "https://us-south.ml.cloud.ibm.com")
API_KEY = os.getenv("IBM_API_KEY")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")

def get_access_token() -> Optional[str]:
    """Exchanges API Key for a Bearer Token (Identity & Access Management)"""
    if not API_KEY:
        return None
        
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = f"grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={API_KEY}"
    
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            return response.json().get("access_token")
        print(f"❌ IBM Auth Failed: {response.text}")
        return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None

def query_granite_model(prompt_text: str) -> Optional[str]:
    """Sends the prompt to the REAL IBM Granite Model"""
    token = get_access_token()
    if not token or not PROJECT_ID:
        return None # Fallback to simulation if no keys
        
    url = f"{IBM_CLOUD_URL}/ml/v1/text/generation?version=2023-05-29"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # The Payload - Strictly formatted for Granite-13b-instruct
    payload = {
        "model_id": "ibm/granite-13b-instruct-v2",
        "input": f"You are a strict municipal AI. Extract data from this text into JSON.\n\nText: {prompt_text}\n\nJSON Output:",
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 0,
            "stop_sequences": ["}"], # Stop when JSON closes
            "repetition_penalty": 1.0
        },
        "project_id": PROJECT_ID
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            # Extract the actual text from IBM's complex JSON response
            return result['results'][0]['generated_text']
        else:
            print(f"⚠️ IBM Granite Error: {response.text}")
            return None
    except Exception as e:
        print(f"⚠️ IBM Granite Connection Failed: {e}")
        return None