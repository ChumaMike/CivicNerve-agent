from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from .mellea_shim import generative  # Our wrapper

# --- Data Models (The "Types" that enforce reliability) ---

class WorkOrder(BaseModel):
    priority: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    department: Literal["ROADS", "WATER", "ELECTRICAL", "PARKS"]
    estimated_budget_usd: int
    required_equipment: List[str]
    safety_notes: str

class IncidentReport(BaseModel):
    summary: str
    location: str
    detected_hazards: List[str]

# --- Generative Functions ---

@generative(model_id="ibm/granite-13b-instruct-v2")
def classify_incident(user_report: str, image_analysis: str) -> IncidentReport:
    """
    Analyze the raw text from a citizen and the description of the attached image.
    Extract the location, summarize the issue, and list specific physical hazards.
    """
    pass # The decorator handles the logic

@generative(model_id="ibm/granite-13b-instruct-v2")
def generate_work_order(incident: IncidentReport, city_blueprint_context: str) -> WorkOrder:
    """
    Act as a Senior City Engineer. Based on the incident and the city's blueprint data,
    create a formal work order.
    
    Rules:
    - If 'water' and 'electricity' are both present, priority must be CRITICAL.
    - Budget must be realistic for municipal repairs.
    """
    pass