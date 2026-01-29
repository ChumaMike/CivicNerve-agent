# src/tools/mellea_shim.py
import functools
import inspect
from typing import get_type_hints

def generative(model_id="ibm/granite-13b-instruct-v2"):
    def decorator(func):
        @functools.wraps(func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"⚡ [Mellea-Smart-Mock] Triggered: {func.__name__}")
            
            # 1. Safely Capture Input (Convert whatever comes in to a lowercase string)
            # This handles both simple text strings AND IncidentReport objects
            user_text = str(args[0]).lower() if args else ""
            
            return_type = inspect.signature(func).return_annotation
            
            # --- SCENARIO 1: THE DANGEROUS BRIBE (Guardian Bait) ---
            if "quick" in user_text or "cheap" in user_text or "ignore" in user_text:
                if func.__name__ == "generate_work_order":
                    return return_type(
                        priority="LOW",
                        department="INTERNAL",
                        estimated_budget_usd=1000000,
                        required_equipment=["None"],
                        safety_notes="None"
                    )

            # --- SCENARIO 2: WATER LEAK (The Hero) ---
            # Added more keywords to be safe: "soweto", "pipe", "burst"
            if any(x in user_text for x in ["water", "burst", "leak", "pipe", "soweto"]):
                if func.__name__ == "classify_incident":
                    return return_type(
                        summary="Major Pipeline Failure Detected",
                        location="Main St & 4th Ave",
                        detected_hazards=["Flooding", "Erosion", "Sinkhole Risk"]
                    )
                if func.__name__ == "generate_work_order":
                    return return_type(
                        priority="CRITICAL",
                        department="WATER",
                        estimated_budget_usd=15000,
                        required_equipment=["Excavator", "Hazmat Suit", "High-Flow Pump"],
                        safety_notes="CRITICAL PROTOCOL:" \
                        " Electrical isolation required. On-site Safety Officer mandated."
                    )

            # --- SCENARIO 3: POTHOLE (Efficiency) ---
            if "pothole" in user_text or "crack" in user_text:
                if func.__name__ == "classify_incident":
                    return return_type(
                        summary="Minor Road Surface Degradation",
                        location="Suburban Road",
                        detected_hazards=["Tyre Damage"]
                    )
                if func.__name__ == "generate_work_order":
                    
                    return return_type(
                        priority="MEDIUM",
                        # ✅ MUST MATCH THE LIST ABOVE EXACTLY:
                        department="GENERAL", 
                        estimated_budget_usd=1000,
                        required_equipment=["Standard Toolkit"],
                        safety_notes="Proceed with caution."
                )

            # --- FALLBACK (CRITICAL FIX) ---
            # If nothing matches, return a GENERIC valid object instead of crashing
            # --- FALLBACK (CRITICAL FIX) ---
            print(f"   ⚠️ No scenario matched. Using Generic Fallback for {func.__name__}")
            
            if func.__name__ == "classify_incident":
                return return_type(
                    summary="General Infrastructure Issue",
                    location="Reported Location",
                    detected_hazards=["Unknown"]
                )
            
            if func.__name__ == "generate_work_order":
                return return_type(
                    priority="MEDIUM",
                    # ✅ CHANGE THIS to match the new list in planner.py
                    department="GENERAL", 
                    estimated_budget_usd=1000,
                    required_equipment=["Standard Toolkit"],
                    safety_notes="Proceed with caution."
                )

            return return_type()
        return wrapper
    return decorator

