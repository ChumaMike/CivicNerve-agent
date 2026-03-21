import sqlite3
import os
import json
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

    # Table 1: Reports — full schema including AI-generated fields
    c.execute('''CREATE TABLE IF NOT EXISTS reports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT,
                    description TEXT,
                    status TEXT DEFAULT 'OPEN',
                    priority TEXT,
                    department TEXT,
                    lat REAL,
                    lon REAL,
                    estimated_budget_zar REAL,
                    work_order_json TEXT,
                    digital_seal TEXT,
                    assigned_crew TEXT,
                    timestamp TEXT
                )''')

    # Table 2: Users / Civic Credits wallet
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    phone TEXT PRIMARY KEY,
                    points INTEGER DEFAULT 0
                )''')

    conn.commit()
    conn.close()


def is_duplicate(description: str, threshold: float = 0.80):
    """
    Checks if a similar report already exists using Jaccard token overlap.
    Returns (True, existing_report_id) or (False, None).
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, description FROM reports ORDER BY id DESC LIMIT 100"
    )
    rows = c.fetchall()
    conn.close()

    desc_tokens = set(description.lower().split())
    if not desc_tokens:
        return False, None

    for report_id, existing_desc in rows:
        if not existing_desc:
            continue
        existing_tokens = set(existing_desc.lower().split())
        union = desc_tokens | existing_tokens
        if not union:
            continue
        overlap = len(desc_tokens & existing_tokens) / len(union)
        if overlap >= threshold:
            return True, report_id

    return False, None


def get_points(phone: str) -> int:
    """Gets Civic Credits balance for a citizen."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT points FROM users WHERE phone=?", (phone,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0


def add_report(
    phone: str,
    description: str,
    points_earned: int,
    work_order=None,
    lat: float = None,
    lon: float = None,
    digital_seal: str = None,
) -> tuple:
    """
    Saves a report with full AI-generated work order data and updates the citizen wallet.
    Returns (ticket_id, new_balance).
    """
    priority = None
    department = None
    estimated_budget = None
    work_order_json = None

    if work_order:
        priority = getattr(work_order, "priority", None)
        department = str(getattr(work_order, "department", None) or "")
        estimated_budget = getattr(work_order, "estimated_budget_zar", None)
        try:
            work_order_json = work_order.model_dump_json()
        except Exception:
            work_order_json = None

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute(
        """INSERT INTO reports
           (phone, description, status, priority, department, lat, lon,
            estimated_budget_zar, work_order_json, digital_seal, timestamp)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            phone, description, "OPEN", priority, department,
            lat, lon, estimated_budget, work_order_json, digital_seal,
            datetime.now().isoformat()
        )
    )
    ticket_id = c.lastrowid

    c.execute("INSERT OR IGNORE INTO users (phone, points) VALUES (?, 0)", (phone,))
    c.execute(
        "UPDATE users SET points = points + ? WHERE phone = ?", (points_earned, phone)
    )
    c.execute("SELECT points FROM users WHERE phone=?", (phone,))
    new_balance = c.fetchone()[0]

    conn.commit()
    conn.close()

    return f"JHB-{1000 + ticket_id}", new_balance


def fetch_all_reports() -> pd.DataFrame:
    """Fetches all reports for the City Ops dashboard."""
    conn = sqlite3.connect(DB_PATH)
    query = """SELECT id, timestamp, phone, description, status,
                      priority, department, estimated_budget_zar, digital_seal
               FROM reports ORDER BY id DESC"""
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def fetch_report_by_id(report_id: int) -> dict:
    """Fetches a single report by its numeric ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT id, phone, description, status, priority, department, "
        "lat, lon, estimated_budget_zar, digital_seal, assigned_crew, timestamp "
        "FROM reports WHERE id=?",
        (report_id,)
    )
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    keys = [
        "id", "phone", "description", "status", "priority", "department",
        "lat", "lon", "estimated_budget_zar", "digital_seal", "assigned_crew", "timestamp"
    ]
    return dict(zip(keys, row))


def update_report_status(report_id: int, status: str, assigned_crew: str = None):
    """Updates the status and optionally assigns a crew to a report."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if assigned_crew:
        c.execute(
            "UPDATE reports SET status=?, assigned_crew=? WHERE id=?",
            (status, assigned_crew, report_id)
        )
    else:
        c.execute("UPDATE reports SET status=? WHERE id=?", (status, report_id))
    conn.commit()
    conn.close()


def get_hotspot_analysis() -> pd.DataFrame:
    """Returns departments with >2 reports in the last 30 days (predictive signal)."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT department, COUNT(*) as report_count,
               AVG(estimated_budget_zar) as avg_cost_zar
        FROM reports
        WHERE timestamp > datetime('now', '-30 days')
          AND department IS NOT NULL
          AND department != ''
        GROUP BY department
        HAVING report_count > 2
        ORDER BY report_count DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
