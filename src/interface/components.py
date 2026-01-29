# src/components.py
import streamlit as st

def render_header():
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/2942/2942544.png", width=80)
    with col2:
        st.title("MyCity Connect")
        st.caption("Report Issues. Earn Points. Build a Better City.")

def render_reward_card(points_earned, total_balance):
    st.markdown(f"""
    <div style="
        padding: 20px;
        background-color: #FFFFFF;
        color: #000000;
        border-radius: 15px;
        border: 2px solid #FFD700;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.3);
        margin-bottom: 20px;">
        <h3 style="color: black; margin:0;">🎉 +{points_earned} Credits Earned!</h3>
        <p style="color: #333; font-size: 16px; margin: 5px 0;">New Balance: <b>{total_balance} 🪙</b></p>
        <p style="color: #666; font-size: 12px;"><em>Redeem at Checkers, Pick n Pay, or for Airtime data!</em></p>
    </div>
    """, unsafe_allow_html=True)

def render_ai_analysis(order):
    """Displays the Engineer's Analysis Card"""
    with st.expander("👀 AI Engineer Analysis", expanded=True):
        c1, c2 = st.columns(2)
        c1.write(f"**Issue:** {order.get('department')} Failure")
        c1.write(f"**Priority:** {order.get('priority')}")
        c2.metric("Est. Cost", f"R {order.get('estimated_budget_zar', 0):,.2f}")
        st.write(f"**Action:** Dispatching {order.get('required_equipment', ['Crew'])[0]}")

def render_legal_check(laws):
    """Displays the RAG Compliance Check"""
    with st.expander("⚖️ Regulatory Compliance (Live RAG)", expanded=True):
        if laws:
            st.markdown("#### 🏛️ Cited Municipal Bylaws:")
            for law in laws:
                clean_law = law.replace("\n", " ").strip()[:200] + "..."
                st.info(f"📜 ...{clean_law}")
            st.caption("✅ Verified against City of Johannesburg Water Services Bylaws (2023)")
        else:
            st.warning("Regulatory check unavailable.")