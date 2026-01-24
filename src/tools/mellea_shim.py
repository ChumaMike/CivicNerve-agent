# src/tools/mellea_shim.py
import os
import json
import functools
import inspect
from typing import Type
from dotenv import load_dotenv
from pydantic import BaseModel
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

# Load Environment Variables
load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
MODEL_ID = os.getenv("WATSONX_MODEL_ID", "ibm/granite-13b-chat-v2")

def get_watson_model():
    """Initialize the connection to IBM Watsonx."""
    if not API_KEY or not PROJECT_ID:
        raise ValueError("❌ Missing WATSONX_API_KEY or WATSONX_PROJECT_ID in .env")

    credentials = Credentials(url=URL, api_key=API_KEY)
    
    # Parameters for strict JSON generation
    params = {
        GenParams.DECODING_METHOD: "greedy",  # Deterministic (best for code/JSON)
        GenParams.MAX_NEW_TOKENS: 500,
        GenParams.MIN_NEW_TOKENS: 10,
        GenParams.REPETITION_PENALTY: 1.1,
        GenParams.STOP_SEQUENCES: ["```", "User:", "\n\n"]
    }

    return ModelInference(
        model_id=MODEL_ID,
        params=params,
        credentials=credentials,
        project_id=PROJECT_ID
    )

def generative(model_id=None):
    """
    The @generative decorator. 
    Converts a Python function into an LLM call using type hints.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 1. Setup Data
            return_type = inspect.signature(func).return_annotation
            schema = return_type.model_json_schema()
            func_docs = func.__doc__
            
            # 2. Build the "System" Prompt for Granite
            # We use a specific prompt engineering pattern for Granite to ensure JSON
            prompt = f"""
            You are a helpful AI Assistant acting as a City Engineer.
            
            TASK: {func_docs}
            
            CONTEXT_DATA: {args} {kwargs}
            
            INSTRUCTIONS:
            1. Analyze the context data.
            2. Output ONLY a valid JSON object.
            3. The JSON must strictly match this schema:
            
            {json.dumps(schema, indent=2)}
            
            RESPONSE (JSON ONLY):
            """
            
            print(f"⚡ [Mellea] Calling Granite 3.0 for: {func.__name__}...")
            
            try:
                # 3. Call IBM Granite
                model = get_watson_model()
                response = model.generate_text(prompt=prompt)
                
                # 4. Clean and Parse Output
                clean_json = response.strip()
                # Remove markdown code blocks if Granite added them
                if clean_json.startswith("```json"):
                    clean_json = clean_json.replace("```json", "").replace("```", "")
                
                print(f"   -> Raw Output: {clean_json[:100]}...") # Debug log
                
                data = json.loads(clean_json)
                
                # 5. Validate & Return Pydantic Object
                return return_type(**data)
                
            except json.JSONDecodeError:
                print(f"❌ [Mellea] Failed to parse JSON from Granite. Response: {response}")
                # In a real hackathon, you might add a retry loop here!
                return return_type() # Return empty/default to prevent crash
            except Exception as e:
                print(f"❌ [Mellea] Watsonx Error: {e}")
                raise e
            
        return wrapper
    return decorator