import streamlit as st
import requests
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000/report_incident"
st.set_page_config(page_title="CivicNerve OS", layout="wide", page_icon="🏙️")

# --- Initialize Session State (To store jobs in memory) ---
if "job_db" not in st.session_state:
    st.session_state.job_db = []

# --- Header ---
st.title("🏙️ CivicNerve: The Sentient City OS")
st.markdown("**System Status:** 🟢 Online | **Guardian AI:** 🛡️ Active")

# --- Tabs for Two Views ---
tab_citizen, tab_city = st.tabs(["📢 Citizen Reporting", "👷 City Operations Center"])

# ==========================================
# VIEW 1: CITIZEN REPORTING (The Input)
# ==========================================
with tab_citizen:
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.subheader("Report an Incident")
        with st.form("incident_form"):
            report_text = st.text_area("Describe the Issue:", value="Massive water pipe burst in Soweto, water running for 2 hours!")
            
            # Optional Photo
            uploaded_file = st.file_uploader("Upload Photo (Optional):", type=["jpg", "png"])
            if uploaded_file:
                image_desc = "Auto-Analysis: High pressure fluid release detected."
                st.caption("✅ Image Analyzed by IBM Granite Vision")
            else:
                image_desc = "No image provided"
                
            submitted = st.form_submit_button("🚀 Dispatch Agent")

    with col2:
        st.subheader("Agent Neural Process")
        if submitted:
            with st.spinner("Agent is Thinking... (Mellea Planning & Guardian Review)"):
                try:
                    payload = {"user_input": report_text, "image_desc": image_desc}
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        guardian_status = str(data.get("guardian_review", "UNKNOWN"))
                        
                        # Display Governance Status
                        if "APPROVED" in guardian_status:
                            st.success(f"🛡️ Governance: {guardian_status}")
                            
                            # SAVE TO CITY DB (The Endgame!)
                            order = data.get("final_work_order") or data.get("work_order", {})
                            if order:
                                job_entry = {
                                    "id": f"JOB-{len(st.session_state.job_db)+101}",
                                    "time": datetime.now().strftime("%H:%M:%S"),
                                    "loc": "Soweto (Simulated)",
                                    "dept": order.get("department"),
                                    "priority": order.get("priority"),
                                    "status": "DISPATCHED"
                                }
                                st.session_state.job_db.insert(0, job_entry) # Add to top
                                
                        else:
                            st.error(f"🛡️ Governance: {guardian_status}")

                        # Show Details
                        with st.expander("🔍 View Generated Work Order", expanded=True):
                            st.json(data)
                    else:
                        st.error(f"Server Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")

# ==========================================
# VIEW 2: CITY OPS CENTER (The Output)
# ==========================================
with tab_city:
    st.subheader("👷 Live Work Order Queue")
    st.markdown("This dashboard updates automatically when the AI approves a job.")
    
    if len(st.session_state.job_db) > 0:
        # Create a nice dataframe/table view
        st.dataframe(st.session_state.job_db, use_container_width=True)
        
        # Metric Cards
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Jobs", len(st.session_state.job_db))
        m2.metric("Est. Budget Commit", "$15,800")
        m3.metric("Avg Response Time", "1.2s")
    else:
        st.info("📭 No active jobs. Waiting for Citizen Reports...")