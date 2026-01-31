import os
import requests
import random
import streamlit as st
from src.data.db_handler import add_report 

# API CONFIG
API_URL = os.getenv("API_URL", "http://localhost:8000")

def submit_report_to_backend(description, image_name):
    """
    Sends the user input to the FastAPI backend.
    """
    payload = {"user_input": description, "image_desc": image_name}
    try:
        # We assume the API is running locally
        response = requests.post(f"{API_URL}/report_incident", json=payload)
        return response.json()
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def fetch_legal_compliance(description):
    """
    Asks the RAG engine for relevant bylaws.
    """
    payload = {"incident_description": description}
    try:
        response = requests.post(f"{API_URL}/consult_bylaws", json=payload)
        if response.status_code == 200:
            return response.json().get("relevant_laws", [])
        return ["Error fetching bylaws."]
    except:
        return ["System Offline"]

def simulate_gps_location():
    """
    Generates a random coordinate in Orlando East, Soweto
    """
    # Center: Orlando East (-26.236, 27.925)
    lat = -26.2360 + (random.uniform(-0.005, 0.005)) 
    lon = 27.9250 + (random.uniform(-0.005, 0.005))
    return lat, lon

def process_successful_report(phone, desc, work_order, lat, lon):
    """
    Saves the job and adds points in one atomic transaction.
    """
    # 1. Determine Points based on Priority
    # (If the AI didn't give a priority, default to MEDIUM)
    priority = work_order.get("priority", "MEDIUM")
    
    points_map = {
        "CRITICAL": 100,
        "HIGH": 75,
        "MEDIUM": 50,
        "LOW": 25
    }
    earned = points_map.get(priority, 50)
    
    # 2. Call the new DB function
    # This handles both saving the ticket and updating the user's wallet
    ticket_id, new_balance = add_report(phone, desc, earned)
    
    return ticket_id, new_balance