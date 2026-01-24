from src.tools.civil_engineer import WorkOrder

class GraniteGuardian:
    def __init__(self):
        # Thresholds for automatic approval
        self.max_budget_low_priority = 5000
        self.max_budget_critical = 50000

    def validate_work_order(self, order: WorkOrder) -> tuple[bool, str]:
        """
        Silent Review: Audits the work order against city policies.
        Returns: (is_approved, reason)
        """
        print(f"🛡️ [Guardian] Auditing Work Order for {order.department}...")

        # Rule 1: Budget Sanity Check
        if order.priority == "LOW" and order.estimated_budget_usd > self.max_budget_low_priority:
            return False, f"REJECTED: Budget ${order.estimated_budget_usd} is too high for LOW priority."

        # Rule 2: Safety Compliance
        if order.priority == "CRITICAL" and "safety" not in order.safety_notes.lower() and "ensure" not in order.safety_notes.lower():
             return False, "REJECTED: Critical orders must have explicit safety protocols detailed."

        # Rule 3: Department Mismatch (Hallucination Check)
        if "water" in str(order.required_equipment).lower() and order.department != "WATER":
             return False, f"REJECTED: Equipment suggests WATER dept, but assigned to {order.department}."

        return True, "APPROVED: Plan meets city governance standards."