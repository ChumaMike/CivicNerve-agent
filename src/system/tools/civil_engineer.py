from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

# ✅ FIX: Connect the Brain Logic
from src.brain.tools.mellea_shim import generative

# --- MCP COMPLIANCE LAYER ---

class DepartmentEnum(str, Enum):
    ROADS = "ROADS"
    WATER = "WATER" 
    ELECTRICAL = "ELECTRICAL"
    PARKS = "PARKS"
    GENERAL = "GENERAL"
    INTERNAL = "INTERNAL" 

class IncidentReport(BaseModel):
    """
    MCP Resource: Represents the raw analysis of the user's input.
    """
    summary: str = Field(description="A one-line technical summary of the issue.")
    location: str = Field(description="Inferred or GPS-tagged location.")
    detected_hazards: List[str] = Field(description="List of immediate risks (e.g., 'Exposed Wire').")

class WorkOrder(BaseModel):
    """
    MCP Resource: Represents the final execution plan for the city.
    """
    priority: str = Field(description="CRITICAL, HIGH, MEDIUM, or LOW.")
    department: DepartmentEnum = Field(description="The municipal unit responsible.")
    estimated_budget_zar: float = Field(description="Cost estimate in South African Rands (ZAR).")
    required_equipment: List[str] = Field(description="Heavy machinery or tools needed.")
    safety_notes: str = Field(description="Mandatory ISO-9001 safety protocols.")

# --- TOOL DEFINITIONS (NOW CONNECTED) ---

@generative()
def classify_incident(user_text: str, image_analysis: str) -> IncidentReport:
    """
    Analyzes raw text and image data to produce a structured incident report.
    """
    pass # The @generative decorator provides the logic!

@generative()
def generate_work_order(incident: IncidentReport, blueprint_context: str) -> WorkOrder:
    """
    Converts an incident report and blueprint data into a costed work order.
    """
    pass # The @generative decorator provides the logic!