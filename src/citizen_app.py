import streamlit as st
import requests
import time
from db_handler import save_job, is_duplicate, add_points, get_points

API_URL = "http://localhost:8000/report_incident"

# --- Page Config ---
st.set_page_config(page_title="MyCity Rewards", page_icon="🇿🇦", layout="centered")

# --- CSS for "Happy" UI ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #00CC66;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .reward-card {
        padding: 20px;
        background-color: #FFFFFF; /* Pure White Background */
        color: #000000; /* Force Black Text */
        border-radius: 15px;
        border: 2px solid #FFD700; /* Gold Border */
        text-align: center;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3); /* Gold Glow */
        margin-bottom: 20px;
    }
    .reward-card h3 {
        color: #000000 !important;
        margin-bottom: 10px;
    }
    .reward-card p {
        color: #333333 !important;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942544.png", width=80)
with col2:
    st.title("MyCity Connect")
    st.caption("Report Issues. Earn Points. Build a Better City.")

# --- Login (Simulated) ---
if "user_phone" not in st.session_state:
    st.info("👋 Welcome! Please enter your number to track your **Civic Credits**.")
    phone = st.text_input("Mobile Number", placeholder="082 123 4567")
    if st.button("Start Reporting"):
        if len(phone) > 5:
            st.session_state.user_phone = phone
            st.rerun()
    st.stop()

# --- Main App (Logged In) ---
# 1. User Wallet Display
my_points = get_points(st.session_state.user_phone)
with st.container():
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        st.subheader(f"Hello, Citizen! 🇿🇦")
    with c3:
        st.metric("Civic Credits", f"{my_points} 🪙")

st.divider()

# 2. The Report Form
st.markdown("### 📸 Spot a problem?")
with st.form("report_form", clear_on_submit=True):
    desc = st.text_area("What's wrong?", placeholder="E.g., Huge pothole on Nelson Mandela Bridge...")
    photo = st.file_uploader("Upload Evidence", type=["jpg", "png"])
    submitted = st.form_submit_button("🚀 Submit & Earn Points")

if submitted:
    if len(desc) < 5:
        st.toast("⚠️ Description is too short!", icon="⚠️")
    else:
        # --- A. CHECK FOR DUPLICATES ---
        is_dup, dup_id = is_duplicate(desc, "Simulated Loc")
        
        if is_dup:
            st.warning(f"🙌 Good eye! Someone else already reported this (Ticket #{dup_id}).")
            st.info("We have boosted the priority of the existing ticket thanks to your confirmation!")
            st.balloons() # Still give balloons for being helpful!
        
        else:
            # --- B. PROCESS NEW REPORT ---
            with st.status("🧠 CivicNerve AI is analyzing...", expanded=True) as status:
                try:
                    # 1. Call Backend API
                    payload = {"user_input": desc, "image_desc": "Photo provided" if photo else "None"}
                    response = requests.post(API_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        guardian = data.get("guardian_review", "UNKNOWN")
                        
                        if "APPROVED" in guardian:
                            order = data.get("final_work_order") or data.get("work_order", {})
                            
                            # 2. Save to DB
                            job_entry = {
                                "description": desc,
                                "location": "Simulated GPS", 
                                "priority": order.get("priority", "MEDIUM"),
                                "budget_usd": order.get("estimated_budget_usd", 0),
                                "department": order.get("department", "GENERAL"),
                                "reporter": st.session_state.user_phone # Track who reported it
                            }
                            ticket_id = save_job(job_entry)
                            
                            # 3. AWARD POINTS
                            new_balance = add_points(st.session_state.user_phone, 50)
                            
                            status.update(label="✅ Success!", state="complete", expanded=False)
                            
                            # --- C. THE HAPPY SUCCESS SCREEN ---
                            st.balloons()
                            st.success(f"**Report Sent! Ticket #{ticket_id}**")
                            
                            # The Reward Card
                            st.markdown(f"""
                            <div class="reward-card">
                                <h3>🎉 +50 Credits Earned!</h3>
                                <p>New Balance: {new_balance} 🪙</p>
                                <p><em>Redeem at Checkers, Pick n Pay, or for Airtime data!</em></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Show AI Analysis
                            with st.expander("👀 See what the AI detected"):
                                st.write(f"**Issue:** {order.get('department')} Failure")
                                st.write(f"**Priority:** {order.get('priority')}")
                                st.write(f"**Action:** Dispatching {order.get('required_equipment', ['Crew'])[0]}")

                        else:
                            status.update(label="❌ Blocked by Safety Shield", state="error")
                            st.error(f"Report rejected: {guardian}")
                            
                except Exception as e:
                    st.error(f"Connection Error: {e}")

# --- Redeem Section ---
with st.expander("🛍️ Spend your Credits"):
    st.write("Use your points for discounts at local partners:")
    c1, c2, c3 = st.columns(3)
    c1.button("🍞 Checkers (500 pts)")
    c2.button("📱 1GB Data (1000 pts)")
    c3.button("🚌 Reya Vaya (200 pts)")