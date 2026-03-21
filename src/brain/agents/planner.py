from typing import TypedDict, List, Any
from src.system.tools.civil_engineer import (
    classify_incident, 
    generate_work_order, 
    IncidentReport, 
    WorkOrder
)

# Define the State (The Data Folder)
class AgentState(TypedDict):
    messages: List[Any]
    incident_report: IncidentReport
    blueprint_data: str
    final_work_order: WorkOrder | None
    guardian_review: str

def create_plan(state: AgentState):
    """
    The Main Logic Chain: Analysis -> Blueprint -> Work Order
    """
    # Defensive check: Ensure messages exist
    user_input = "Unknown Issue"
    if state["messages"] and len(state["messages"]) > 0:
        user_input = state["messages"][0][1] 
    
    # --- STEP 1: READ BLUEPRINTS ---
    print("\n🔹 [Step 1] Sensory Cortex: Reading Blueprints...")
    # Blueprint context — default zone profile; extend with GIS integration later
    blueprint_context = (
        "Zone 4: Mixed Residential/Industrial. High traffic. "
        "Grid-connected infrastructure. Proximity to Soweto water mains."
    )
    
    # --- STEP 2: CLASSIFY INCIDENT ---
    print("\n🔹 [Step 2] Frontal Lobe: Analyzing Incident...")
    # We pass the RAW TEXT to the classifier
    incident_data = classify_incident(user_input, "No Image")
    
    # --- STEP 3: GENERATE WORK ORDER ---
    print("\n🔹 [Step 3] Motor Cortex: Generating Work Order...")
    # Now we pass the CLASSIFIED incident to the generator
    order = generate_work_order(incident_data, blueprint_context)
    
    print(f"   -> Proposed: Dispatch {order.department} (Budget: R{order.estimated_budget_zar:,})")
    
    return {
        "incident_report": incident_data,
        "final_work_order": order,
        "blueprint_data": blueprint_context
    }