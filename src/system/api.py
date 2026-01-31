from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.brain.agents.planner import create_plan, AgentState
from src.system.tools.civil_engineer import IncidentReport
from src.brain.rag_engine import query_knowledge_base
from src.governance.guardian import GraniteGuardian

app = FastAPI(title="CivicNerve API", version="2.1")

class IncidentRequest(BaseModel):
    user_input: str
    image_desc: Optional[str] = "None"

class BylawRequest(BaseModel):
    incident_description: str

@app.post("/report_incident")
def report_incident(request: IncidentRequest):
    print(f"📥 Received Report: {request.user_input}")
    
    # 1. Prepare the State
    state = AgentState(
        messages=[("user", request.user_input)],
        incident_report=IncidentReport(
            summary="Pending", location="Unknown", detected_hazards=[]
        ),
        blueprint_data="Pending",
        final_work_order=None,
        guardian_review="Pending"
    )
    
    try:
        # 2. CALL PLANNER (Granite Optimized)
        result = create_plan(state) 
        
        # 3. Run Guardian Check (Enterprise Audit)
        guardian = GraniteGuardian()
        if result["final_work_order"]:
            audit_log = guardian.audit_plan(result["final_work_order"])
            
            # Simple logic for frontend compatibility
            review_summary = audit_log["status"]
            if audit_log["status"] != "APPROVED":
                review_summary = f"{audit_log['status']}: {audit_log['reason']}"
        else:
            audit_log = {"status": "ERROR", "reason": "No Plan Generated"}
            review_summary = "ERROR: No Plan Generated"
            
        return {
            "status": "processed",
            "work_order": result["final_work_order"],
            "guardian_review": review_summary,
            "audit_trail": audit_log # ✅ SENDING THE DIGITAL SEAL TO FRONTEND
        }

    except Exception as e:
        print(f"❌ API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/consult_bylaws")
def consult_bylaws(request: BylawRequest):
    """RAG Endpoint for Legal Checks"""
    try:
        laws = query_knowledge_base(request.incident_description)
        return {"status": "success", "relevant_laws": laws}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Launching CivicNerve Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)