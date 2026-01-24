from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

# Define the State of the Agent
class AgentState(TypedDict):
    user_input: str
    image_desc: str
    blueprint_data: str
    incident_report: dict
    final_work_order: dict
    error: str

# Define Nodes (The steps the agent takes)
def ingest_data(state: AgentState):
    print("🧠 [Brain] Step 1: Ingesting Data...")
    # Logic to call Docling would go here
    return {"blueprint_data": "Mock blueprint data: Main St Water Main (1985)"}

def analyze_risk(state: AgentState):
    print("🧠 [Brain] Step 2: Analyzing Risk (Calling Civil Engineer Tool)...")
    # Logic to call Mellea/CivilEngineer would go here
    return {"incident_report": {"summary": "Broken Pipe", "location": "Main St"}}

def create_plan(state: AgentState):
    print("🧠 [Brain] Step 3: Creating Work Order...")
    return {"final_work_order": {"priority": "HIGH", "budget": 500}}

# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("ingest", ingest_data)
workflow.add_node("analyze", analyze_risk)
workflow.add_node("plan", create_plan)

workflow.set_entry_point("ingest")
workflow.add_edge("ingest", "analyze")
workflow.add_edge("analyze", "plan")
workflow.add_edge("plan", END)

app = workflow.compile()