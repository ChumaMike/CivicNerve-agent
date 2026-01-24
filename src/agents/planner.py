from typing import TypedDict
from langgraph.graph import StateGraph, END
from src.tools.civil_engineer import classify_incident, generate_work_order, IncidentReport, WorkOrder
from src.governance.guardian import GraniteGuardian

# Initialize the Guardian
guardian = GraniteGuardian()

class AgentState(TypedDict):
    user_input: str
    image_desc: str
    blueprint_data: str
    incident_report: IncidentReport | None
    final_work_order: WorkOrder | None
    guardian_feedback: str

# --- Nodes ---

def ingest_data(state: AgentState):
    print("\n🔹 [Step 1] Sensory Cortex: Reading Blueprints...")
    return {"blueprint_data": "Blueprint #8842: 12-inch Cast Iron Main"}

def analyze_risk(state: AgentState):
    print("\n🔹 [Step 2] Frontal Lobe: Analyzing Incident...")
    report = classify_incident(state["user_input"], state["image_desc"])
    print(f"   -> Detected: {report.summary}")
    return {"incident_report": report}

def create_plan(state: AgentState):
    print("\n🔹 [Step 3] Motor Cortex: Generating Work Order...")
    order = generate_work_order(state["incident_report"], state["blueprint_data"])
    
    # HACK: Let's force a "Bad" plan to test the Guardian!
    # Uncomment the line below to see the Guardian REJECT the plan.
    # order.priority = "LOW"; order.estimated_budget_usd = 100000 
    
    print(f"   -> Proposed: Dispatch {order.department} (Budget: ${order.estimated_budget_usd})")
    return {"final_work_order": order}

def governance_review(state: AgentState):
    print("\n🔹 [Step 4] Guardian Lobe: Silent Review...")
    order = state["final_work_order"]
    
    approved, reason = guardian.validate_work_order(order)
    
    if approved:
        print(f"   ✅ {reason}")
        return {"guardian_feedback": "APPROVED"}
    else:
        print(f"   ❌ {reason}")
        # In a real agent, we would loop back to 'create_plan' with this feedback!
        return {"guardian_feedback": reason}

# --- Graph ---

workflow = StateGraph(AgentState)

workflow.add_node("ingest", ingest_data)
workflow.add_node("analyze", analyze_risk)
workflow.add_node("plan", create_plan)
workflow.add_node("guardian", governance_review) # New Node!

workflow.set_entry_point("ingest")
workflow.add_edge("ingest", "analyze")
workflow.add_edge("analyze", "plan")
workflow.add_edge("plan", "guardian")
workflow.add_edge("guardian", END)

app = workflow.compile()