from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.planner import app as agent_app

app = FastAPI(
    title="CivicNerve API",
    description="Autonomous Agent for City Infrastructure Maintenance",
    version="1.0.0"
)

class ReportRequest(BaseModel):
    user_input: str
    image_desc: str = "No image provided"

@app.get("/")
def health_check():
    return {"status": "online", "system": "CivicNerve v1"}

@app.post("/report_incident")
def report_incident(request: ReportRequest):
    """
    Trigger the Autonomous Agent Loop.
    """
    print(f"📥 Received Report: {request.user_input}")
    
    initial_state = {
        "user_input": request.user_input,
        "image_desc": request.image_desc,
        "blueprint_data": "",
        "incident_report": None,
        "final_work_order": None,
        "guardian_feedback": ""
    }
    
    try:
        # Run the LangGraph Agent
        result = agent_app.invoke(initial_state)
        
        # Extract the final output
        work_order = result.get("final_work_order")
        guardian_status = result.get("guardian_feedback")
        
        if not work_order:
             raise HTTPException(status_code=500, detail="Agent failed to generate plan")

        return {
            "status": "success",
            "guardian_review": guardian_status,
            "incident": result.get("incident_report"),
            "work_order": work_order
        }
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Launching CivicNerve Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)