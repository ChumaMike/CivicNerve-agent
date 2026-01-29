import requests
import random
import streamlit as st
from src.data.db_handler import save_job, add_points

API_URL = "http://localhost:8000"

def simulate_gps_location():
    """Generates a random coordinate in Orlando West, Soweto"""
    # Center Point: Orlando West (-26.2323, 27.9138)
    # We add small variation so points don't stack perfectly
    lat = -26.2323 + (random.uniform(-0.005, 0.005)) 
    lon = 27.9138 + (random.uniform(-0.005, 0.005))
    return lat, lon

def submit_report_to_backend(description, image_name):
    """Sends the report to the AI Brain"""
    payload = {"user_input": description, "image_desc": image_name}
    try:
        response = requests.post(f"{API_URL}/report_incident", json=payload)
        if response.status_code == 200:
            return response.json()
        return {"error": f"Server Error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def fetch_legal_compliance(description):
    """Consults the RAG Engine for Bylaws"""
    try:
        response = requests.post(f"{API_URL}/consult_bylaws", json={"incident_description": description})
        if response.status_code == 200:
            return response.json().get("relevant_laws", [])
        return []
    except:
        return []

def process_successful_report(user_phone, desc, ai_order, lat, lon):
    """Saves the job to SQL and awards points"""
    # 1. Prepare Data
    job_entry = {
        "description": desc,
        "location": f"{lat:.4f}, {lon:.4f}",
        "priority": ai_order.get("priority", "MEDIUM"),
        "budget_zar": ai_order.get("estimated_budget_zar", 0),
        "department": ai_order.get("department", "GENERAL"),
        "reporter": user_phone
    }
    
    # 2. Save to DB
    ticket_id = save_job(job_entry)
    
    # 3. Add Points
    new_balance = add_points(user_phone, 50)
    
    return ticket_id, new_balance