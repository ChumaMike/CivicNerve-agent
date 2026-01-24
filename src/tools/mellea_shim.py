import functools
import inspect
import json
from pydantic import BaseModel

def generative(model_id="ibm/granite-13b-instruct-v2"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"⚡ [Mellea] Generative Slot Triggered: {func.__name__}")
            
            # Get the return type class (e.g., IncidentReport)
            return_type = inspect.signature(func).return_annotation
            
            # --- MOCK LOGIC (Simulates Granite) ---
            # In the real version, we send 'prompt' to Watsonx and parse the JSON.
            # Here, we return a valid dummy object based on the function name.
            
            if func.__name__ == "classify_incident":
                return return_type(
                    summary="High pressure water main fracture detected",
                    location="Intersection of Main St and 4th Ave",
                    detected_hazards=["Flooding", "Erosion", "Slippery Surface"]
                )
                
            if func.__name__ == "generate_work_order":
                return return_type(
                    priority="CRITICAL",
                    department="WATER",
                    estimated_budget_usd=12500,
                    required_equipment=["Excavator", "Pipe Clamps", "Water Pump"],
                    safety_notes="Ensure electricity is cut off before digging."
                )

            # Fallback for other functions
            return return_type()
            
        return wrapper
    return decorator