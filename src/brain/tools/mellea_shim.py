import functools
import inspect
from typing import get_type_hints

def generative(model_id="ibm/granite-13b-instruct-v2"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"⚡ [Mellea-Smart-Mock] Triggered: {func.__name__}")
            
            # 1. Capture Inputs
            user_text = str(args[0]).lower() if args else ""
            
            # Capture the return type so we know what object to build
            return_type = inspect.signature(func).return_annotation
            
            # --- SCENARIO 1: THE DANGEROUS BRIBE (Guardian Bait) ---
            if "quick" in user_text or "cheap" in user_text or "ignore" in user_text:
                if func.__name__ == "generate_work_order":
                    return return_type(
                        priority="LOW",
                        department="INTERNAL",
                        # ✅ FIXED: Renamed to ZAR and increased value
                        estimated_budget_zar=20000000, 
                        required_equipment=["None"],
                        safety_notes="None"
                    )

            # --- SCENARIO 2: WATER LEAK (The Hero) ---
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
                        # ✅ FIXED: Renamed to ZAR (approx R270k)
                        estimated_budget_zar=270000,
                        required_equipment=["Excavator", "Hazmat Suit", "High-Flow Pump"],
                        safety_notes="CRITICAL PROTOCOL: Electrical isolation required. On-site Safety Officer mandated."
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
                        department="GENERAL", 
                        # ✅ FIXED: Renamed to ZAR (approx R15k)
                        estimated_budget_zar=15000,
                        required_equipment=["Standard Toolkit"],
                        safety_notes="Proceed with caution."
                    )
                
                # --- SCENARIO 4: PARKS / TREES (The Green Scorpions) ---
            if any(x in user_text for x in ["tree", "branch", "grass", "park", "fallen"]):
                if func.__name__ == "classify_incident":
                    return return_type(
                        summary="Vegetation Obstruction Detected",
                        location="Orlando East",
                        detected_hazards=["Road Blockage", "Power Line Risk"]
                    )
                if func.__name__ == "generate_work_order": 
                    return return_type(
                        priority="MEDIUM",
                        department="PARKS", 
                        estimated_budget_zar=8500,
                        required_equipment=["Chainsaw", "Wood Chipper", "Flatbed Truck"],
                        safety_notes="Ensure area is cordoned off from pedestrians."
                    )

            # --- SCENARIO 5: CRIME / SECURITY (JMPD) ---
            if any(x in user_text for x in ["steal", "gun", "fight", "crime", "robbery", "hijack"]):
                if func.__name__ == "classify_incident":
                    return return_type(
                        summary="Active Security Threat Reported",
                        location="User Location",
                        detected_hazards=["Violence", "Public Safety Risk"]
                    )
                if func.__name__ == "generate_work_order": 
                    return return_type(
                        priority="CRITICAL",
                        department="GENERAL", # Or add "POLICE" to your Enums later
                        estimated_budget_zar=0, # Police service is free/funded differently
                        required_equipment=["Patrol Vehicle", "Backup Unit"],
                        safety_notes="Dispatch JMPD immediately. Do not send unarmed engineers."
                    )

            # --- FALLBACK (Safety Net) ---
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
                    department="GENERAL", 
                    # ✅ FIXED: Renamed to ZAR
                    estimated_budget_zar=5000,
                    required_equipment=["Standard Toolkit"],
                    safety_notes="Proceed with caution."
                )

            return return_type()
        return wrapper
    return decorator