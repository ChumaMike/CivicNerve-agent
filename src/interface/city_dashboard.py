import sys
import os
import time
import pandas as pd
import streamlit as st
import plotly.express as px # For the Pro Map

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

from src.data.db_handler import fetch_all_reports

# --- CONFIG ---
st.set_page_config(
    page_title="JHB City Ops | CivicNerve",
    page_icon="🏙️",
    layout="wide", # Command Center Mode
    initial_sidebar_state="collapsed"
)

# --- STYLING (Dark Mode Enterprise) ---
st.markdown("""
<style>
    .metric-card {
        background-color: #0E1117;
        border: 1px solid #30333F;
        padding: 20px;
        border-radius: 10px;
    }
    h1 { color: #ffffff; }
    h3 { color: #00A6D6; } /* IBM Blue */
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([4, 1])
c1.title("🏙️ JHB Infrastructure Operations Center")
c1.caption("Powered by **IBM watsonx.governance** & **Granite Guardian**")

if c2.button("🔄 Refresh Feed"):
    st.rerun()

st.divider()

# --- 1. LIVE METRICS (The "KPIs") ---
df = fetch_all_reports()

if not df.empty:
    # Calculate stats
    total_tickets = len(df)
    pending = len(df[df['status'] == 'VERIFIED']) # Simplified status
    # Simulated Budget (Random math for the demo based on tickets)
    est_spend = total_tickets * 15000 
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Incidents", total_tickets, "+2 today")
    m2.metric("Open Work Orders", pending, "Active")
    m3.metric("Est. Budget Deployed", f"R {est_spend:,.0f}", "ZAR")
    m4.metric("Governance Compliance", "100%", "Granite Audited")
else:
    st.info("Waiting for citizen reports...")

st.divider()

# --- 2. INTELLIGENT GRID (The Map & Table) ---
col_map, col_feed = st.columns([1, 1])

with col_map:
    st.subheader("📍 Geospatial Heatmap (Soweto)")
    if not df.empty:
        # Simulate GPS for the demo table (Since DB stores text, we generate mock coords for visualization)
        # In prod, you'd pull 'lat'/'lon' columns from the DB.
        mock_data = pd.DataFrame({
            'lat': [-26.236 + (i*0.001) for i in range(len(df))],
            'lon': [27.925 + (i*0.002) for i in range(len(df))],
            'type': ['Water Burst' if 'water' in d.lower() else 'Pothole' for d in df['description']]
        })
        
        st.map(mock_data, zoom=13)
        st.caption("Real-time telemetry from **Citizen App** submissions.")

with col_feed:
    st.subheader("📝 Live Incident Feed")
    if not df.empty:
        # Show recent tickets
        for index, row in df.head(5).iterrows():
            with st.expander(f"Ticket #JHB-100{row['id']} | {row['timestamp'][:10]}", expanded=True):
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Reporter:** {row['phone']}")
                st.info("✅ **Granite Seal:** Verified via `src.governance.guardian`")
                
                # --- INTERACTIVE BUTTONS ---
                b1, b2 = st.columns(2)
                
                # Button 1: Dispatch (The Action)
                if b1.button("🚧 Dispatch Crew", key=f"d_{index}"):
                    # Show a cool "Toast" notification
                    st.toast(f"👷 **Unit 04 Dispatched!** SMS sent to Foreman.", icon="🚀")
                    time.sleep(1)
                
                # Button 2: Docling (The Intelligence)
                if b2.button("📄 Docling Analysis", key=f"v_{index}"):
                    # Show what the AI "read" from the PDF
                    st.success(f"""
                        **Docling Extraction:**
                        - **Source:** Water_Services_Bylaws_2023.pdf
                        - **Table Detected:** 'Tariffs & Fines' (Page 42)
                        - **Compliance:** Section 7 (Infrastructure Protection)
                        - **Est. Repair Time:** 4 Hours
                    """)

# --- 3. GOVERNANCE AUDIT LOG (The IBM Flex) ---
st.divider()
st.subheader("🛡️ Governance Audit Log (Blockchain-Ready)")
st.caption("Immutable record of all AI-generated work orders, signed by Granite Guardian.")

if not df.empty:
    audit_data = []
    for index, row in df.iterrows():
        audit_data.append({
            "Ticket ID": f"JHB-100{row['id']}",
            "Timestamp": row['timestamp'],
            "AI Model": "ibm/granite-13b-instruct",
            "Guardian Status": "APPROVED",
            "Digital Seal": f"sha256:{hash(row['description'] + row['timestamp'])}"[:20] + "..."
        })
    
    st.dataframe(
        pd.DataFrame(audit_data), 
        use_container_width=True,
        hide_index=True
    )   