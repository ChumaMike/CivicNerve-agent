import streamlit as st
import pandas as pd
from data.db_handler import get_jobs, update_status

st.set_page_config(page_title="CityOps Command", layout="wide", page_icon="🏢")

# --- 1. SIMULATED AUTHENTICATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.title("🔒 CityOps Secure Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and pwd == "joburg":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials (Try: admin / joburg)")
    st.stop()

# --- 2. MAIN DASHBOARD ---
st.sidebar.title(f"👮 Officer: {st.session_state.get('user', 'Admin')}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.title("🏢 Johannesburg Operations Center")
st.markdown(f"**Live Feed:** {len(get_jobs())} Incidents Recorded")

# Load Data
jobs = get_jobs()

if not jobs:
    st.info("No active incidents.")
else:
    for job in jobs:
        # Card Layout for each Job
        with st.container(border=True):
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1.5])
            
            with c1:
                st.subheader(f"{job['id']}: {job['department']}")
                st.write(f"📍 {job['description']}")
                st.caption(f"🕒 Reported: {job['timestamp']}")
            
            with c2:
                # Priority Badge
                if job['priority'] == "CRITICAL":
                    st.error("CRITICAL")
                elif job['priority'] == "HIGH":
                    st.warning("HIGH")
                else:
                    st.info(job['priority'])
                
                # STATUS
                st.write(f"**Status:** {job['status']}")

            with c3:
                # Budget in RANDS (Assume 1 USD = 18 ZAR)
                rands = job['budget_usd'] * 18
                st.metric("Est. Budget", f"R {rands:,.0f}")
            
            with c4:
                st.write("**Dispatch Options:**")
                
                if job['status'] == "PENDING REVIEW":
                    # Dynamic Dispatch Buttons based on Dept
                    crew_options = []
                    if job['department'] == "WATER":
                        crew_options = ["Joburg Water Unit 4", "Emergency Plumbers"]
                    elif job['department'] == "ROADS":
                        crew_options = ["JRA Tar Team", "Contractor: PaveSmart"]
                    else:
                        crew_options = ["General Maintenance A", "Rapid Response"]
                        
                    crew = st.selectbox("Select Crew", crew_options, key=f"sel_{job['id']}")
                    
                    if st.button(f"🚀 Dispatch {crew}", key=f"btn_{job['id']}"):
                        update_status(job['id'], "DISPATCHED", crew)
                        st.success(f"Crew dispatched to {job['id']}")
                        st.rerun()
                        
                elif job['status'] == "DISPATCHED":
                    st.success(f"🚚 Crew En Route: {job.get('assigned_crew')}")
                    if st.button("Mark Resolved", key=f"res_{job['id']}"):
                         update_status(job['id'], "RESOLVED")
                         st.rerun()
                else:
                    st.success("✅ Issue Resolved")