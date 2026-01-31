import sys
import os
import time
import pytest

# 🛠️ SENIOR FIX: Add the project root to Python's search path
# This tells Python: "Look one level up from this file to find 'src'"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- IMPORTS FROM YOUR PROJECT ---
from src.governance.guardian import GraniteGuardian
from src.system.tools.civil_engineer import generate_work_order, IncidentReport, WorkOrder, DepartmentEnum
from src.data.db_handler import init_db, add_report, get_points

# --- TEST 1: THE BRAIN (Integration Test) ---
def test_mellea_shim_generative_flow():
    """
    Does the Generative Kernel intercept the real tool and return Water logic?
    """
    print("\n🧪 Testing Mellea Kernel Integration...")

    # 1. Create a Fake Incident that contains the trigger word "WATER"
    # The Shim reads args[0], so it will see "water" in the summary.
    trigger_incident = IncidentReport(
        summary="Major water pipe burst detected", 
        location="Soweto",
        detected_hazards=["Flooding"]
    )

    # 2. Call the REAL tool
    # The @generative decorator intercepts this call!
    result = generate_work_order(trigger_incident, "Blueprint: Water Infrastructure")
    
    # 3. Validation
    # If the Shim works, it returns a WorkOrder, NOT None.
    assert isinstance(result, WorkOrder), "Shim returned wrong type!"
    
    # It should detect "WATER" context and return the WATER department
    assert result.department == DepartmentEnum.WATER
    assert result.priority == "CRITICAL"
    print("✅ Mellea Kernel correctly intercepted tool and identified 'Water' context.")

# --- TEST 2: THE GUARDIAN (Safety Logic) ---
def test_guardian_safety_block():
    """
    Does the Guardian block unsafe electrical work?
    """
    print("\n🧪 Testing Granite Guardian...")
    guardian = GraniteGuardian()
    
    # Create a DANGEROUS work order (High Voltage, No Gloves)
    unsafe_order = WorkOrder(
        priority="CRITICAL",
        department=DepartmentEnum.ELECTRICAL,
        estimated_budget_zar=50000,
        required_equipment=["Standard Toolkit"], # Missing Gloves!
        safety_notes="Just fix it quickly"
    )
    
    audit = guardian.audit_plan(unsafe_order)
    
    assert audit["status"] == "BLOCKED"
    assert "Safety Violation" in audit["reason"]
    print("✅ Guardian successfully blocked unsafe electrical work.")

# --- TEST 3: THE DATABASE (Persistence) ---
def test_database_transactions():
    """
    Does the DB save tickets and update points?
    Uses a unique user ID to ensure a clean test every time.
    """
    print("\n🧪 Testing SQLite Transactions...")
    init_db()
    
    # SENIOR FIX: Generate a unique user ID using timestamp
    # This prevents "previous run" data from breaking the test
    unique_phone = f"082-TEST-{int(time.time())}"
    
    # 1. Check initial state (Should be 0)
    initial_points = get_points(unique_phone)
    assert initial_points == 0, "New user should start with 0 points"
    
    # 2. Add Report (Earn 50 pts)
    # The unique ID ensures we are adding to a fresh wallet
    ticket_id, new_balance = add_report(unique_phone, "Test Pothole", 50)
    
    # 3. Validations
    assert "JHB-" in ticket_id
    assert new_balance == 50
    assert get_points(unique_phone) == 50
    
    print(f"✅ Database committed Ticket {ticket_id} for User {unique_phone}.")
    print(f"   ↳ Balance Verified: {new_balance} Points.")

if __name__ == "__main__":
    # Allow running this file directly
    test_mellea_shim_generative_flow()
    test_guardian_safety_block()
    test_database_transactions()
    print("\n🎉 ALL SYSTEMS GO: Core Logic is Solid.")