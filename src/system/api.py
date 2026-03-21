import os
import asyncio
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.data.db_handler import (
    init_db, fetch_all_reports, fetch_report_by_id,
    update_report_status, is_duplicate
)
from src.agents.orchestrator import CivicOrchestrator
from src.brain.tools.language_bridge import normalize_to_english
from src.system.logger import get_logger
from src.system.notifications import send_ticket_confirmation

logger = get_logger(__name__)
security = HTTPBearer(auto_error=False)

# Rate limiter — 10 reports per minute per IP
limiter = Limiter(key_func=get_remote_address)

# Module-level orchestrator (instantiated once at startup)
orchestrator: CivicOrchestrator = None

CITY_OPS_TOKEN = os.getenv("CITY_OPS_TOKEN", "")
VECTOR_DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../../src/data/vector_db"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator
    logger.info("CivicNerve API starting up")
    init_db()
    orchestrator = CivicOrchestrator()
    logger.info("Database and orchestrator initialized")
    yield
    logger.info("CivicNerve API shutting down")


app = FastAPI(title="CivicNerve API", version="3.0", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# --- Request/Response Models ---

class IncidentRequest(BaseModel):
    user_input: str
    image_desc: Optional[str] = "None"
    phone: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

class BylawRequest(BaseModel):
    incident_description: str

class StatusUpdateRequest(BaseModel):
    status: str
    assigned_crew: Optional[str] = None


# --- Auth helper ---

def require_city_ops(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if not CITY_OPS_TOKEN:
        raise HTTPException(status_code=503, detail="City ops token not configured.")
    if not credentials or credentials.credentials != CITY_OPS_TOKEN:
        raise HTTPException(status_code=403, detail="Unauthorized.")


# --- Endpoints ---

@app.get("/health")
def health_check():
    checks = {
        "api": "ok",
        "ibm_api_key": "ok" if os.getenv("IBM_API_KEY") else "missing",
        "ibm_project_id": "ok" if os.getenv("IBM_PROJECT_ID") else "missing",
        "vector_db": "ok" if os.path.exists(VECTOR_DB_PATH) else "missing — run python -m src.brain.rag_engine"
    }
    status_code = 200 if all(v == "ok" for v in checks.values()) else 503
    return JSONResponse(content=checks, status_code=status_code)


@app.post("/report_incident")
@limiter.limit("10/minute")
async def report_incident(request: Request, body: IncidentRequest):
    logger.info("Incident received", extra={"input": body.user_input[:80]})

    # Multilingual normalization
    english_input, detected_lang = normalize_to_english(body.user_input)
    if detected_lang != "en":
        logger.info("Language detected", extra={"lang": detected_lang})

    # Duplicate detection — award bonus points to confirming citizens
    is_dup, dup_id = is_duplicate(english_input)
    base_points = 10
    if is_dup:
        base_points = 25  # Bonus for confirming an existing report
        logger.info("Duplicate report detected", extra={"original_id": dup_id})

    try:
        # Run the full agentic pipeline in a thread pool (non-blocking)
        result = await asyncio.get_event_loop().run_in_executor(
            None, orchestrator.run, english_input, body.image_desc or "None", detected_lang
        )

        work_order = result.get("work_order")
        audit_trail = result.get("audit_trail", {})
        guardian_status = result.get("guardian_review", "ERROR")
        bylaws = result.get("relevant_bylaws", [])

        # Persist report with full work order data
        digital_seal = audit_trail.get("digital_seal")
        ticket_id, new_balance = None, 0
        if body.phone:
            from src.data.db_handler import add_report
            ticket_id, new_balance = add_report(
                phone=body.phone,
                description=body.user_input,
                points_earned=base_points,
                work_order=work_order,
                lat=body.lat,
                lon=body.lon,
                digital_seal=digital_seal
            )

            # Send SMS confirmation if approved
            if guardian_status == "APPROVED" and work_order and ticket_id:
                dept = str(getattr(work_order, "department", "General"))
                send_ticket_confirmation(body.phone, ticket_id, dept)

        review_summary = guardian_status
        if guardian_status not in ("APPROVED", "ERROR"):
            review_summary = f"{guardian_status}: {audit_trail.get('reason', '')}"

        return {
            "status": "processed",
            "ticket_id": ticket_id,
            "civic_credits_earned": base_points,
            "new_balance": new_balance,
            "is_duplicate_boost": is_dup,
            "detected_language": detected_lang,
            "work_order": work_order,
            "guardian_review": review_summary,
            "audit_trail": audit_trail,
            "relevant_bylaws": bylaws
        }

    except Exception as e:
        logger.error("API pipeline error", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/consult_bylaws")
async def consult_bylaws(request: BylawRequest):
    """RAG endpoint for querying relevant city bylaws."""
    try:
        from src.brain.rag_engine import query_knowledge_base
        laws = await asyncio.get_event_loop().run_in_executor(
            None, query_knowledge_base, request.incident_description
        )
        return {"status": "success", "relevant_laws": laws}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports/{ticket_id}")
def get_report_status(ticket_id: str):
    """Citizen-facing: check status of a submitted report."""
    try:
        numeric_id = int(ticket_id.replace("JHB-", "")) - 1000
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format (expected JHB-XXXX).")
    report = fetch_report_by_id(numeric_id)
    if not report:
        raise HTTPException(status_code=404, detail="Ticket not found.")
    return report


@app.get("/reports")
def list_reports(_: None = Depends(require_city_ops)):
    """City ops: full incident feed (requires bearer token)."""
    df = fetch_all_reports()
    return df.to_dict("records") if not df.empty else []


@app.patch("/reports/{ticket_id}/status")
def update_status(
    ticket_id: str,
    body: StatusUpdateRequest,
    _: None = Depends(require_city_ops)
):
    """City ops: update status and optionally assign a crew."""
    try:
        numeric_id = int(ticket_id.replace("JHB-", "")) - 1000
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ticket ID format.")
    update_report_status(numeric_id, body.status, body.assigned_crew)
    return {"status": "updated", "ticket_id": ticket_id}


@app.get("/stats/summary")
def stats_summary():
    """Aggregated KPIs for the operations dashboard."""
    df = fetch_all_reports()
    if df.empty:
        return {"total_incidents": 0, "by_status": {}, "by_department": {}, "total_budget_zar": 0}

    by_status = df["status"].value_counts().to_dict() if "status" in df.columns else {}
    by_dept = df["department"].value_counts().to_dict() if "department" in df.columns else {}
    total_budget = (
        df["estimated_budget_zar"].dropna().sum()
        if "estimated_budget_zar" in df.columns else 0
    )

    return {
        "total_incidents": len(df),
        "by_status": by_status,
        "by_department": by_dept,
        "total_budget_zar": round(total_budget, 2)
    }


if __name__ == "__main__":
    import uvicorn
    logger.info("Launching CivicNerve API server")
    uvicorn.run(app, host="0.0.0.0", port=8000)
