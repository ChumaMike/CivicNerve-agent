# src/tools/mellea_shim.py
import functools
import inspect
from typing import get_type_hints

def generative(model_id="ibm/granite-13b-instruct-v2"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"⚡ [Mellea-Mock] Generative Slot Triggered: {func.__name__}")
            
            # Get the return type class
            return_type = inspect.signature(func).return_annotation
            
            # --- MOCK LOGIC (Simulates Granite) ---
            if func.__name__ == "classify_incident":
                print("   -> Simulating Vision Analysis...")
                return return_type(
                    summary="High pressure water main fracture detected (Simulated)",
                    location="Intersection of Main St and 4th Ave",
                    detected_hazards=["Flooding", "Erosion", "Slippery Surface"]
                )
                
            if func.__name__ == "generate_work_order":
                print("   -> Simulating Engineering Plan...")
                return return_type(
                    priority="CRITICAL",
                    department="WATER",
                    estimated_budget_usd=12500,
                    required_equipment=["Excavator", "Pipe Clamps", "Water Pump"],
                    safety_notes="Ensure electricity is cut off before digging."
                )

            # Fallback
            return return_type()
        return wrapper
    return decorator