import sys
import os
import time

# Get the absolute path to the project root (Go up 2 levels from src/interface)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

import streamlit as st
import random
from src.data.db_handler import is_duplicate, get_points
import src.system.services as services
import src.interface.components as components

# --- CONFIG & STYLING ---
st.set_page_config(page_title="MyCity Rewards", page_icon="🇿🇦", layout="centered")
components.render_header()

# --- LOGIN ---
if "user_phone" not in st.session_state:
    st.info("👋 Welcome! Please enter your number to track your **Civic Credits**.")
    phone = st.text_input("Mobile Number", placeholder="082 123 4567")
    if st.button("Start Reporting"):
        if len(phone) > 5:
            st.session_state.user_phone = phone
            st.rerun()
    st.stop()

# --- DASHBOARD ---
my_points = get_points(st.session_state.user_phone)
with st.container():
    c1, c3 = st.columns([3, 1])
    c1.subheader(f"Hello, Citizen! 🇿🇦")
    c3.metric("Civic Credits", f"{my_points} 🪙")
st.divider()

# --- REPORT FORM ---
# Only show the form if we are NOT showing a success message
if "success_data" not in st.session_state:
    st.markdown("### 📸 Spot a problem?")
    with st.form("report_form", clear_on_submit=True):
        desc = st.text_area("What's wrong?", placeholder="E.g., Huge pothole on Nelson Mandela Bridge...")
        
        st.write("**Evidence:**")
        tab1, tab2 = st.tabs(["📸 Take Photo", "📂 Upload File"])
        with tab1: cam_photo = st.camera_input("Snap a picture")
        with tab2: file_photo = st.file_uploader("Choose from gallery", type=["jpg", "png"])
        photo = cam_photo if cam_photo else file_photo

        submitted = st.form_submit_button("🚀 Submit & Earn Points")

    if submitted:
        if len(desc) < 5:
            st.toast("⚠️ Description too short!")
        else:
            # Check Duplicates
            is_dup, dup_id = is_duplicate(desc)
            if is_dup:
                st.warning(f"🙌 Good eye! Already reported (Ticket #{dup_id}). Priority boosted!")
                st.balloons()
            else:
                # We use a Status Container to show the AI's "Brain Waves"
                with st.status("🚀 CivicNerve Agents Activating...", expanded=True) as status:
                    
                    # Step 1: Ingestion
                    st.write("👀 **Sensory Cortex:** Analyzing Evidence...")
                    time.sleep(1) # Fake delay for drama
                    
                    # Call the API
                    image_name = photo.name if photo else "None"
                    api_result = services.submit_report_to_backend(desc, image_name)
                    
                    if "error" in api_result:
                        status.update(label="❌ System Error", state="error")
                        st.error(api_result["error"])
                    else:
                        # Step 2: Planning
                        st.write("🧠 **Planner Agent:** Consulting Municipal Blueprints (Granite Optimized)...")
                        time.sleep(0.8)
                        
                        guardian = api_result.get("guardian_review", "UNKNOWN")
                        audit_trail = api_result.get("audit_trail", {})
                        
                        if "APPROVED" in guardian:
                            # Step 3: Governance
                            st.write(f"🛡️ **Granite Guardian:** Auditing Budget & Safety...")
                            time.sleep(0.8)
                            st.write(f"   ↳ 🔐 Digital Seal Generated: `{audit_trail.get('digital_seal', 'UNKNOWN')}`")
                            
                            # Step 4: Finalizing
                            st.write("💰 **Finance Layer:** Allocating ZAR Budget...")
                            time.sleep(0.5)

                            # Success Logic
                            order = api_result.get("work_order") or api_result.get("final_work_order", {})
                            lat, lon = services.simulate_gps_location()
                            
                            # Save & Pay
                            ticket_id, new_balance = services.process_successful_report(
                                st.session_state.user_phone, desc, order, lat, lon
                            )
                            
                            # ✅ SAVE DATA TO STATE
                            st.session_state["success_data"] = {
                                "ticket_id": ticket_id,
                                "balance": new_balance,
                                "lat": lat, "lon": lon,
                                "order": order,
                                "laws": services.fetch_legal_compliance(desc),
                                "audit": audit_trail # Save the Audit for the receipt
                            }
                            
                            status.update(label="✅ **Work Order Authorized!**", state="complete", expanded=False)
                            time.sleep(1.5) # Let them admire the green checkmark
                            st.rerun() # NOW we refresh
                            
                        else:
                            status.update(label="❌ **Guardian Rejected Plan**", state="error")
                            st.error(f"Governance Block: {guardian}")
                            st.write(f"Reason: {audit_trail.get('reason', 'Unknown')}")

# --- SUCCESS SCREEN---
else:
    # If we have success data, show THIS instead of the form
    data = st.session_state["success_data"]
    
    st.balloons()
    components.render_reward_card(50, data["balance"])
    st.success(f"**Report Sent! Ticket #{data['ticket_id']}**")
    
    st.map({"lat": [data["lat"]], "lon": [data["lon"]]})
    components.render_ai_analysis(data["order"])
    components.render_legal_check(data["laws"])
    
    st.divider()
    if st.button("⬅️ Report Another Issue"):
        # Clear memory and reload to show the form again
        del st.session_state["success_data"]
        st.rerun()
        
# --- REDEEM SECTION ---
with st.expander("🛍️ Spend your Credits"):
    st.write("Use your points for discounts at local partners:")
    c1, c2, c3 = st.columns(3)
    c1.button("🍞 Checkers (500 pts)")
    c2.button("📱 1GB Data (1000 pts)")
    c3.button("🚌 Reya Vaya (200 pts)")