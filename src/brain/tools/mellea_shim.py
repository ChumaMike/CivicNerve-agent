import functools
import inspect
import json
from typing import get_type_hints, Any

# --- IMPORTS FOR REAL AI (The "All In" Upgrade) ---
# We try to import the gateway. If it fails (file missing), we use a dummy function.
try:
    from src.brain.gateways.ibm_service import query_granite_model
except ImportError:
    print("⚠️ Warning: IBM Gateway not found. Running in Offline Mode.")
    query_granite_model = lambda x: None 

# --- CONFIGURATION ---
MODEL_ID = "ibm/granite-13b-instruct-v2"

def generative(model_id=MODEL_ID):
    """
    Implements the 'Generative Computing' pattern (Talk 22).
    Interleaves Classical Logic (Rules) with Generative AI (Granite).
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            
            # 1. Capture Inputs (The "Context")
            user_text = str(args[0]).lower() if args else ""
            return_type = inspect.signature(func).return_annotation
            
            print(f"⚡ [Mellea Kernel] Executing Generative Program: '{func_name}'")
            print(f"   ↳ 🧠 Model: {model_id} (Hybrid Mode: Real + Simulation)")
            
            # --- LAYER 1: CLASSICAL LOGIC (Deterministic Governance) ---
            # We run this BEFORE the AI to save cost/tokens and ensure safety.
            
            # Rule A: The "Dangerous Bribe" Trap
            if "quick" in user_text or "cheap" in user_text or "ignore" in user_text:
                print(f"   ↳ 🛡️ [Classical Rule Triggered]: Governance Violation Pattern Detected.")
                if func_name == "generate_work_order":
                    return return_type(
                        priority="LOW",
                        department="INTERNAL",
                        estimated_budget_zar=20000000, # Trap Value
                        required_equipment=["None"],
                        safety_notes="None"
                    )

            # --- LAYER 2: REAL IBM GRANITE AI (The "All In" Upgrade) ---
            # We attempt to call the actual API.
            
            prompt = f"""
            Act as a City Infrastructure AI.
            Task: {func_name}
            Input: "{user_text}"
            
            Return ONLY a valid JSON object matching the schema.
            """
            
            # Try the Real AI
            granite_response = query_granite_model(prompt)
            '.'

            if granite_response:
                try:
                    # Clean up the response (Granite sometimes adds extra chars)
                    clean_json = granite_response.strip()
                    if not clean_json.endswith("}"): clean_json += "}"
                    
                    data = json.loads(clean_json)
                    print("   ↳ 🧠 IBM Granite Response Received & Parsed!")
                    
                    # Validate against Pydantic model
                    return return_type(**data) 
                except Exception as e:
                    print(f"   ↳ ⚠️ Granite produced invalid JSON ({e}). Switching to Simulation Fallback.")
            
            # --- LAYER 3: SIMULATION FALLBACK (Classical Heuristics) ---
            #If the Real AI fails (or no API key), we use these robust heuristics.
            print("   ↳ 🛡️ Using Classical Logic (Simulation Mode)")

            # Scenario: Water Infrastructure (Granite Context: Fluid Dynamics)
            if any(x in user_text for x in ["water", "burst", "leak", "pipe", "soweto"]):
                if func_name == "classify_incident":
                    return return_type(
                        summary="Major Pipeline Failure Detected",
                        location="Main St & 4th Ave (Inferred)",
                        detected_hazards=["Flooding", "Erosion", "Sinkhole Risk"]
                    )
                if func_name == "generate_work_order":
                    return return_type(
                        priority="CRITICAL",
                        department="WATER",
                        estimated_budget_zar=270000,
                        required_equipment=["Excavator", "Hazmat Suit", "High-Flow Pump"],
                        safety_notes="CRITICAL PROTOCOL: Electrical isolation required. On-site Safety Officer mandated."
                    )

            # Scenario: Green Infrastructure (Granite Context: Vegetation)
            if any(x in user_text for x in ["tree", "branch", "grass", "park", "fallen"]):
                if func_name == "classify_incident":
                    return return_type(
                        summary="Vegetation Obstruction Detected",
                        location="Orlando East",
                        detected_hazards=["Road Blockage", "Power Line Risk"]
                    )
                if func_name == "generate_work_order": 
                    return return_type(
                        priority="MEDIUM",
                        department="PARKS", 
                        
                        estimated_budget_zar=8500,
                        required_equipment=["Chainsaw", "Wood Chipper", "Flatbed Truck"],
                        safety_notes="Ensure area is cordoned off from pedestrians."
                )

            # Scenario: Electrical Danger (Granite Context: High Voltage)
            if any(x in user_text for x in ["wire", "danger", "box", "substation", "electricity"]):
                if func_name == "generate_work_order":
                    return return_type(
                        priority="CRITICAL",
                        department="ELECTRICAL",
                        estimated_budget_zar=450000, 
                        required_equipment=["Insulated Gloves", "Arc Suit", "Lockout Kit"],
                        safety_notes="CRITICAL: Do not approach. Police escort required."
                    )
            
            # Scenario: Public Safety / Crime (Granite Context: JMPD Protocol)
            if any(x in user_text for x in ["steal", "gun", "fight", "crime", "robbery", "hijack"]):
                if func_name == "classify_incident":
                     return return_type(
                        summary="Active Security Threat Reported",
                        location="User Location",
                        detected_hazards=["Violence", "Public Safety Risk"]
                    )
                if func_name == "generate_work_order": 
                    return return_type(
                        priority="CRITICAL",
                        department="GENERAL", 
                        estimated_budget_zar=0, # JMPD Service
                        required_equipment=["Patrol Vehicle", "Backup Unit"],
                        safety_notes="Dispatch JMPD immediately. Do not send unarmed engineers."
                )

            # Scenario: Road Infrastructure (Granite Context: Civil Engineering)
            if "pothole" in user_text or "crack" in user_text:
                if func_name == "classify_incident":
                    return return_type(
                        summary="Minor Road Surface Degradation",
                        location="Suburban Road",
                        detected_hazards=["Tyre Damage"]
                    )
                if func_name == "generate_work_order": 
                    return return_type(
                        priority="MEDIUM",
                        department="GENERAL", 
                        estimated_budget_zar=15000,
                        required_equipment=["Standard Toolkit", "Bitumen"],
                        safety_notes="Proceed with caution."
                )

            # --- FALLBACK (The Hallucination Safety Net) ---
            print(f"   ⚠️ [Generative Fallback] Input unclear. Defaulting to general protocol.")
            
            if func_name == "classify_incident":
                return return_type(
                    summary="General Infrastructure Issue",
                    location="Reported Location",
                    detected_hazards=["Unknown"]
                )
            
            if func_name == "generate_work_order":
                return return_type(
                    priority="MEDIUM",
                    department="GENERAL", 
                    estimated_budget_zar=5000,
                    required_equipment=["Standard Toolkit"],
                    safety_notes="Proceed with caution."
                )

            return return_type()
        return wrapper
    return decorator