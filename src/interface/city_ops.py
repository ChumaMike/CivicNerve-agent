"""
Legacy city ops file — superseded by city_dashboard.py (docker-compose uses city_dashboard.py).
This file is kept for backwards compatibility but redirects to the new dashboard.
"""
import streamlit as st

st.set_page_config(page_title="CityOps", layout="wide", page_icon="🏢")
st.warning(
    "This interface has been upgraded. "
    "Please use the **City Dashboard** at port 8502 (`city_dashboard.py`)."
)
st.info("Run: `streamlit run src/interface/city_dashboard.py --server.port 8502`")
