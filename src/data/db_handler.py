import sqlite3
import os
from datetime import datetime
from difflib import SequenceMatcher

DB_FILE = "civic_nerve.db"

def init_db():
    """Initialize a Relational SQL Database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # 1. Users Table (The Wallet)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, 
                  points INTEGER DEFAULT 0,
                  joined_date TEXT)''')
    
    # 2. Incidents Table (The Work Orders)
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (id TEXT PRIMARY KEY,
                  timestamp TEXT,
                  description TEXT,
                  location TEXT,
                  department TEXT,
                  priority TEXT,
                  budget_zar INTEGER,
                  status TEXT,
                  reporter_phone TEXT,
                  assigned_crew TEXT)''')
    
    conn.commit()
    conn.close()

# --- WALLET FUNCTIONS ---
def add_points(phone, amount=50):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Check if user exists, if not create them
    c.execute("SELECT points FROM users WHERE phone=?", (phone,))
    result = c.fetchone()
    
    if result:
        new_points = result[0] + amount
        c.execute("UPDATE users SET points=? WHERE phone=?", (new_points, phone))
    else:
        new_points = amount
        c.execute("INSERT INTO users (phone, points, joined_date) VALUES (?, ?, ?)", 
                  (phone, amount, datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()
    return new_points

def get_points(phone):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE phone=?", (phone,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

# --- INCIDENT FUNCTIONS ---
def save_job(job_data):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Generate ID: JHB-1001, JHB-1002...
    c.execute("SELECT COUNT(*) FROM incidents")
    count = c.fetchone()[0]
    job_id = f"JHB-{count + 1001}"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    c.execute('''INSERT INTO incidents VALUES 
                 (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (job_id, timestamp, job_data['description'], job_data['location'],
               job_data['department'], job_data['priority'], job_data['budget_zar'],
               "PENDING REVIEW", job_data['reporter'], "None"))
    
    conn.commit()
    conn.close()
    return job_id

def is_duplicate(description):
    init_db()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Fetch all active descriptions
    c.execute("SELECT id, description FROM incidents WHERE status != 'RESOLVED'")
    rows = c.fetchall()
    conn.close()
    
    for row in rows:
        ticket_id, text = row
        similarity = SequenceMatcher(None, text.lower(), description.lower()).ratio()
        if similarity > 0.6:
            return True, ticket_id
            
    return False, None

# For the City Ops Dashboard
def get_jobs():
    init_db()
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    c = conn.cursor()
    c.execute("SELECT * FROM incidents ORDER BY timestamp DESC")
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return rows