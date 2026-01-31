from brain.agents.planner import app

# Simulate a run
initial_state = {
    "user_input": "There is a massive leak on Main St!",
    "image_desc": "Water gushing from pavement",
    "blueprint_data": "",
    "incident_report": {},
    "final_work_order": {},
    "error": ""
}

print("🚀 Starting CivicNerve Agent...")
result = app.invoke(initial_state)
print("✅ Agent Finished. Final State:", result)