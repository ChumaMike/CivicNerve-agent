from typing import Dict, Any

class GraniteGuardian:
    def __init__(self):
        # In a real scenario, this initiates the specific Granite Guardian model
        self.banned_keywords = ["fake", "scam", "ignore previous instructions"]

    def validate_input(self, text: str) -> bool:
        """Check for prompt injection or toxicity."""
        if any(word in text.lower() for word in self.banned_keywords):
            return False
        return True

    def validate_output(self, work_order: Dict[str, Any]) -> bool:
        """
        Silent Review: Ensure the agent isn't hallucinating crazy budgets.
        """
        budget = work_order.get("estimated_budget_usd", 0)
        priority = work_order.get("priority", "LOW")

        # Business Logic Guardrail
        if priority == "LOW" and budget > 50000:
            print(f"🛡️ [Guardian] BLOCKED: High budget ({budget}) for LOW priority task.")
            return False
            
        return True