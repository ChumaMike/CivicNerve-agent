from src.system.tools.civil_engineer import WorkOrder

class GraniteGuardian:
    def __init__(self):
        self.name = "Granite Guardian"

    def audit_plan(self, work_order: WorkOrder) -> str:
        """
        The 'Silent Review' step. Checks safety and budget before approval.
        """
        print(f"🛡️ [Guardian] Auditing Work Order for {work_order.department}...")
        
        # 1. Safety Check (High Voltage Rule)
        if work_order.department == "ELECTRICAL":
            has_gloves = any("gloves" in item.lower() for item in work_order.required_equipment)
            has_isolation = "isolation" in work_order.safety_notes.lower()
            
            if not (has_gloves or has_isolation):
                return "BLOCKED: Electrical work requires insulated gloves or isolation protocol."

        # 2. Budget Check (ZAR Limit)
        # We allow up to R2,000,000 for emergency infrastructure
        if work_order.estimated_budget_zar > 2000000:
            return f"BLOCKED: Budget R{work_order.estimated_budget_zar} exceeds municipal limit of R2m."

        # 3. Equipment Check
        if not work_order.required_equipment:
            return "BLOCKED: No equipment specified for repair crew."

        print("   ✅ APPROVED: Plan meets city governance standards.")
        return "APPROVED"