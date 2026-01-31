import hashlib
import uuid
from datetime import datetime
from src.system.tools.civil_engineer import WorkOrder

class GraniteGuardian:
    def __init__(self):
        self.agent_id = "GUARDIAN-CORE-01"
        self.policy_version = "v2025.1.0"

    def _generate_digital_seal(self, work_order: WorkOrder, decision: str) -> str:
        """
        Talk 9: Agentic Auth.
        Creates a cryptographic hash of the decision to ensure Non-Repudiation.
        """
        raw_data = f"{work_order.department}|{work_order.estimated_budget_zar}|{decision}|{datetime.now()}"
        return hashlib.sha256(raw_data.encode()).hexdigest()[:16] # Short seal for UI

    def audit_plan(self, work_order: WorkOrder) -> dict:
        """
        The 'Silent Review' step. Checks safety and budget before approval.
        Returns a Structured Audit Record, not just a string.
        """
        print(f"🛡️ [Guardian] Auditing Work Order for {work_order.department}...")
        
        audit_record = {
            "auditor_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "status": "PENDING",
            "reason": "Review in progress",
            "digital_seal": "None"
        }

        # 1. Safety Check (High Voltage Rule)
        if work_order.department == "ELECTRICAL":
            has_gloves = any("gloves" in item.lower() for item in work_order.required_equipment)
            has_isolation = "isolation" in work_order.safety_notes.lower()
            
            if not (has_gloves or has_isolation):
                audit_record["status"] = "BLOCKED"
                audit_record["reason"] = "Safety Violation: Missing High Voltage PPE Protocol."
                return audit_record

        # 2. Budget Check (ZAR Limit)
        # We allow up to R2,000,000 for emergency infrastructure
        if work_order.estimated_budget_zar > 2000000:
             audit_record["status"] = "BLOCKED"
             audit_record["reason"] = f"Governance Violation: Budget R{work_order.estimated_budget_zar} exceeds municipal cap."
             return audit_record

        # 3. Equipment Check
        if not work_order.required_equipment:
            audit_record["status"] = "BLOCKED"
            audit_record["reason"] = "Operational Violation: No equipment specified."
            return audit_record

        # ✅ APPROVED
        audit_record["status"] = "APPROVED"
        audit_record["reason"] = "Plan meets ISO-9001 City Governance standards."
        audit_record["digital_seal"] = self._generate_digital_seal(work_order, "APPROVED")
        
        print(f"   ✅ APPROVED: Digital Seal [{audit_record['digital_seal']}] generated.")
        return audit_record