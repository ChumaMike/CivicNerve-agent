import sqlite3
import os
from datetime import datetime
import pandas as pd

# Path setup
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DB_PATH = os.path.join(PROJECT_ROOT, "src/data/civic_nerve.db")

def init_db():
    """Creates the database and tables if they don't exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Table 1: Reports
    c.execute('''CREATE TABLE IF NOT EXISTS reports
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  phone TEXT, 
                  description TEXT, 
                  status TEXT, 
                  timestamp TEXT)''')
    
    # Table 2: Users (The missing table!)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (phone TEXT PRIMARY KEY, 
                  points INTEGER)''')
    
    conn.commit()
    conn.close()

def is_duplicate(description):
    """
    DEMO MODE: Always allow reports (returns False).
    """
    return False, None

def get_points(phone):
    """
    Gets points for a user. 
    ✅ FIX: Auto-initializes DB if file was deleted.
    """
    init_db()  # <--- THIS IS THE FIX. RUNS EVERY TIME.
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE phone=?", (phone,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def add_report(phone, description, points_earned):
    """
    Saves report and updates wallet in one go.
    """
    init_db() # Double check DB exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # 1. Log report
    c.execute("INSERT INTO reports (phone, description, status, timestamp) VALUES (?, ?, ?, ?)",
              (phone, description, "VERIFIED", datetime.now().isoformat()))
    ticket_id = c.lastrowid
    
    # 2. Add points
    c.execute("INSERT OR IGNORE INTO users (phone, points) VALUES (?, 0)", (phone,))
    c.execute("UPDATE users SET points = points + ? WHERE phone = ?", (points_earned, phone))
    
    # 3. Get new balance
    c.execute("SELECT points FROM users WHERE phone=?", (phone,))
    new_balance = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    return f"JHB-{1000+ticket_id}", new_balance


def fetch_all_reports():
    """
    CITY OPS: Fetches live data for the Dashboard.
    Returns a Pandas DataFrame for easy table rendering.
    """
    init_db()
    conn = sqlite3.connect(DB_PATH)
    
    # We join with users to get point info if needed, but simple is fine for now
    query = "SELECT id, timestamp, phone, description, status FROM reports ORDER BY id DESC"
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df