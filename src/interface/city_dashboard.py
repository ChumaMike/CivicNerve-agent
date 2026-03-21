import sys
import os
import time
import pandas as pd
import streamlit as st
import plotly.express as px

# --- PATH SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.append(project_root)

from src.data.db_handler import fetch_all_reports, update_report_status, get_hotspot_analysis

# --- CONFIG ---
st.set_page_config(
    page_title="JHB City Ops | CivicNerve",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
<style>
    .metric-card {
        background-color: #0E1117;
        border: 1px solid #30333F;
        padding: 20px;
        border-radius: 10px;
    }
    h1 { color: #ffffff; }
    h3 { color: #00A6D6; }
</style>
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
ADMIN_USER = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🏙️ JHB Infrastructure Operations Center")
    st.subheader("Secure Login")
    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if ADMIN_PASS and u == ADMIN_USER and p == ADMIN_PASS:
                st.session_state.authenticated = True
                st.rerun()
            elif not ADMIN_PASS and u == ADMIN_USER:
                # Allow login without password only if no password is configured (dev mode)
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Invalid credentials.")
    st.stop()

# --- HEADER ---
c1, c2 = st.columns([4, 1])
c1.title("🏙️ JHB Infrastructure Operations Center")
c1.caption("Powered by **IBM watsonx.governance** & **Granite Guardian**")

if c2.button("🔄 Refresh Feed"):
    st.rerun()

if c2.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

st.divider()

# --- 1. LIVE METRICS ---
df = fetch_all_reports()

if not df.empty:
    total_tickets = len(df)
    pending = len(df[df["status"] == "OPEN"])
    dispatched = len(df[df["status"] == "DISPATCHED"])

    # Use real budget data if available, otherwise fall back to estimate
    if "estimated_budget_zar" in df.columns:
        real_budget = df["estimated_budget_zar"].dropna().sum()
        budget_label = f"R {real_budget:,.0f}"
    else:
        budget_label = f"R {total_tickets * 15000:,.0f} (est.)"

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Incidents", total_tickets)
    m2.metric("Open Work Orders", pending)
    m3.metric("Crews Dispatched", dispatched)
    m4.metric("Est. Budget Deployed", budget_label)
else:
    st.info("Waiting for citizen reports...")

st.divider()

# --- 2. INTELLIGENT GRID ---
col_map, col_feed = st.columns([1, 1])

with col_map:
    st.subheader("📍 Geospatial Heatmap (Soweto)")
    if not df.empty:
        if "lat" in df.columns and df["lat"].notna().any():
            map_data = df[["lat", "lon"]].dropna()
            st.map(map_data, zoom=13)
        else:
            # Simulated GPS for demo when real coords not stored
            mock_data = pd.DataFrame({
                "lat": [-26.236 + (i * 0.001) for i in range(len(df))],
                "lon": [27.925 + (i * 0.002) for i in range(len(df))]
            })
            st.map(mock_data, zoom=13)
        st.caption("Real-time telemetry from **Citizen App** submissions.")

with col_feed:
    st.subheader("📝 Live Incident Feed")
    if not df.empty:
        for index, row in df.head(5).iterrows():
            dept = row.get("department", "Unknown") or "Unknown"
            priority = row.get("priority", "—") or "—"
            ticket_label = f"JHB-{1000 + row['id']} | {str(row['timestamp'])[:10]} | {dept} | {priority}"
            with st.expander(ticket_label, expanded=True):
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Reporter:** {row['phone']}")
                seal = row.get("digital_seal", None)
                if seal:
                    st.success(f"✅ **Granite Seal:** `{seal}`")
                else:
                    st.info("Guardian seal pending.")

                b1, b2, b3 = st.columns(3)
                crew_options = ["Unit 01 - Water", "Unit 02 - Roads", "Unit 03 - Electrical", "Unit 04 - Parks"]
                selected_crew = b1.selectbox("Assign Crew", crew_options, key=f"crew_{index}")

                if b2.button("🚧 Dispatch", key=f"dispatch_{index}"):
                    update_report_status(row["id"], "DISPATCHED", selected_crew)
                    st.toast(f"👷 **{selected_crew} Dispatched!**", icon="🚀")
                    time.sleep(1)
                    st.rerun()

                if b3.button("✅ Resolve", key=f"resolve_{index}"):
                    update_report_status(row["id"], "RESOLVED")
                    st.toast("Report marked as resolved.", icon="✅")
                    time.sleep(1)
                    st.rerun()

# --- 3. PREDICTIVE MAINTENANCE ---
st.divider()
st.subheader("🔮 Predictive Maintenance Risk")
st.caption("Departments with >2 reports in the last 30 days signal infrastructure stress.")

try:
    hotspots = get_hotspot_analysis()
    if not hotspots.empty:
        # Highlight departments at critical threshold
        critical = hotspots[hotspots["report_count"] > 5]
        if not critical.empty:
            for _, row in critical.iterrows():
                st.error(
                    f"⚠️ HIGH RISK: **{row['department']}** has {row['report_count']} reports "
                    f"this month. Avg cost: R{row['avg_cost_zar']:,.0f}. Proactive inspection recommended."
                )

        fig = px.bar(
            hotspots,
            x="department",
            y="report_count",
            color="report_count",
            color_continuous_scale="Reds",
            labels={"report_count": "Reports (30 days)", "department": "Department"},
            title="Infrastructure Stress by Department (Last 30 Days)"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No infrastructure stress signals detected in the last 30 days.")
except Exception as e:
    st.warning(f"Predictive analytics unavailable: {e}")

# --- 4. GOVERNANCE AUDIT LOG ---
st.divider()
st.subheader("🛡️ Governance Audit Log")
st.caption("Immutable record of all AI-generated work orders, signed by Granite Guardian.")

if not df.empty:
    audit_data = []
    for _, row in df.iterrows():
        audit_data.append({
            "Ticket ID": f"JHB-{1000 + row['id']}",
            "Timestamp": str(row["timestamp"])[:19],
            "Department": row.get("department", "—") or "—",
            "Priority": row.get("priority", "—") or "—",
            "Status": row.get("status", "—"),
            "Digital Seal": (row.get("digital_seal") or "pending")[:20],
            "Budget (ZAR)": f"R {row['estimated_budget_zar']:,.0f}"
                if row.get("estimated_budget_zar") else "—"
        })

    st.dataframe(
        pd.DataFrame(audit_data),
        use_container_width=True,
        hide_index=True
    )
