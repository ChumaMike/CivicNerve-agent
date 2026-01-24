import os
from dotenv import load_dotenv
from ibm_watsonx_ai import APIClient, Credentials

# 1. Force reload the .env file
load_dotenv(override=True)

api_key = os.getenv("WATSONX_API_KEY")
project_id = os.getenv("WATSONX_PROJECT_ID")
url = os.getenv("WATSONX_URL")

print(f"🔎 DEBUG: Checking credentials...")
print(f"   API Key Length: {len(api_key) if api_key else 'None'}")
print(f"   Project ID: {project_id}")
print(f"   URL: {url}")

if not api_key or len(api_key) < 10:
    print("❌ ERROR: API Key looks too short or is missing!")
    exit(1)

try:
    print("\n☁️ Connecting to IBM Cloud...")
    credentials = Credentials(url=url, api_key=api_key)
    client = APIClient(credentials)
    
    # Try to list models to prove access
    print("✅ Authentication Success! Fetching available models...")
    models = client.foundation_models.get_model_specs()
    print(f"🎉 Success! Found {len(models['resources'])} models available.")
    
except Exception as e:
    print(f"\n❌ FATAL AUTH ERROR: {e}")