import json
import os
from datetime import datetime
from difflib import SequenceMatcher

DB_FILE = "jobs_db.json"
USERS_FILE = "users_db.json"

# --- 1. DATABASE INITIALIZATION ---
def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)

# --- 2. JOB MANAGEMENT FUNCTIONS ---
def get_jobs():
    init_db()
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_job(job_data):
    init_db()
    with open(DB_FILE, "r") as f:
        jobs = json.load(f)
    
    # Create unique ID and timestamp
    job_data["id"] = f"JHB-{len(jobs)+1001}"
    job_data["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    job_data["status"] = "PENDING REVIEW"
    
    jobs.insert(0, job_data) # Add to top of list
    
    with open(DB_FILE, "w") as f:
        json.dump(jobs, f, indent=4)
    return job_data["id"]

# --- 3. CITY OPS FUNCTIONS (This was missing!) ---
def update_status(job_id, new_status, crew_assigned=None):
    init_db()
    with open(DB_FILE, "r") as f:
        jobs = json.load(f)
    
    for job in jobs:
        if job["id"] == job_id:
            job["status"] = new_status
            if crew_assigned:
                job["assigned_crew"] = crew_assigned
                
    with open(DB_FILE, "w") as f:
        json.dump(jobs, f, indent=4)

# --- 4. GAMIFICATION FUNCTIONS ---
def is_duplicate(description, location_simulated):
    init_db()
    jobs = get_jobs()
    for job in jobs:
        # Check similarity > 60%
        text_similarity = SequenceMatcher(None, job["description"].lower(), description.lower()).ratio()
        if text_similarity > 0.6 and job["status"] not in ["RESOLVED", "REJECTED"]:
            return True, job["id"]
    return False, None

def add_points(user_phone, amount=50):
    init_db()
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    
    current_points = users.get(user_phone, 0)
    users[user_phone] = current_points + amount
    
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)
    return users[user_phone]

def get_points(user_phone):
    init_db()
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
    return users.get(user_phone, 0)