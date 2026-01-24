from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.tools.civil_engineer import classify_incident, generate_work_order, IncidentReport, WorkOrder

# Define the State of the Agent
class AgentState(TypedDict):
    user_input: str
    image_desc: str
    blueprint_data: str
    incident_report: IncidentReport | None  # Now strictly typed!
    final_work_order: WorkOrder | None      # Now strictly typed!
    error: str

# --- The Nodes (Steps) ---

def ingest_data(state: AgentState):
    print("\n🔹 [Step 1] Sensory Cortex: Reading Blueprints...")
    # (We will hook up Docling here later)
    return {"blueprint_data": "Blueprint #8842: 12-inch Cast Iron Main, Depth 4ft."}

def analyze_risk(state: AgentState):
    print("\n🔹 [Step 2] Frontal Lobe: Analyzing Incident...")
    
    # CALLING THE TOOL (Mellea)
    report = classify_incident(
        user_report=state["user_input"], 
        image_analysis=state["image_desc"]
    )
    
    print(f"   -> Detected: {report.summary} at {report.location}")
    return {"incident_report": report}

def create_plan(state: AgentState):
    print("\n🔹 [Step 3] Motor Cortex: Generating Work Order...")
    
    # CALLING THE TOOL (Mellea)
    order = generate_work_order(
        incident=state["incident_report"], 
        city_blueprint_context=state["blueprint_data"]
    )
    
    print(f"   -> Action: Dispatch {order.department} Dept. (Priority: {order.priority})")
    return {"final_work_order": order}

# --- The Graph ---

workflow = StateGraph(AgentState)
workflow.add_node("ingest", ingest_data)
workflow.add_node("analyze", analyze_risk)
workflow.add_node("plan", create_plan)

workflow.set_entry_point("ingest")
workflow.add_edge("ingest", "analyze")
workflow.add_edge("analyze", "plan")
workflow.add_edge("plan", END)

app = workflow.compile()