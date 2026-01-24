import streamlit as st
import requests
import json

API_URL = "http://0.0.0.0:8000/report_incident"
st.set_page_config(page_title="CivicNerve Command Center", layout="wide", page_icon="🏙️")

st.title("🏙️ CivicNerve: Autonomous City Infrastructure")
st.markdown("**Status:** 🟢 Online | **Guardian Protocol:** 🛡️ Active")
st.divider()

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("📢 New Incident Report")
    with st.form("incident_form"):
        report_text = st.text_area("Describe the Issue:", value="Water main burst at 42nd St.")
        image_desc = st.text_input("Visual Analysis (Simulated):", value="High pressure water visible.")
        submitted = st.form_submit_button("🚀 Dispatch Agent")

with col2:
    st.subheader("🧠 Agent Neural Process")
    
    if submitted:
        with st.spinner("Agent is Thinking... (Mellea Planning & Guardian Review)"):
            try:
                # Call your own API
                payload = {"user_input": report_text, "image_desc": image_desc}
                response = requests.post(API_URL, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # 1. Guardian Check
                    if "APPROVED" in str(data.get("guardian_review")):
                        st.success(f"🛡️ Governance: {data['guardian_review']}")
                    else:
                        st.error(f"🛡️ Governance: {data['guardian_review']}")

                    # 2. Tabs for details
                    tab1, tab2 = st.tabs(["📋 Work Order", "🔍 Raw Analysis"])
                    
                    with tab1:
                        order = data.get("work_order", {})
                        st.info(f"**Priority:** {order.get('priority')}")
                        st.warning(f"**Dept:** {order.get('department')}")
                        st.write(f"**Budget:** ${order.get('estimated_budget_usd')}")
                        st.write(f"**Equipment:** {', '.join(order.get('required_equipment', []))}")
                    
                    with tab2:
                        st.json(data)
                        
                else:
                    st.error(f"Server Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed. Is the API running? {e}")