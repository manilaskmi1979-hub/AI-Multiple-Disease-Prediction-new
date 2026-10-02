"""
db.py
-----
Tiny SQLite storage for the simple Name + Phone login and prediction history.
The database file (app.db) is created automatically on first run.
"""

import json
import os
import re
import sqlite3
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "app.db")


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS users (
                        phone TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        last_login TEXT NOT NULL)""")
        c.execute("""CREATE TABLE IF NOT EXISTS predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        age INTEGER,
                        symptoms TEXT,
                        top_result TEXT,
                        probabilities TEXT)""")


def validate_login(name, phone):
    """Returns (clean_name, clean_phone, error). error is None when valid."""
    name = " ".join((name or "").split())
    phone = re.sub(r"[\s\-]", "", phone or "")
    if phone.startswith("+91"):
        phone = phone[3:]
    elif phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]

    if len(name) < 2 or not re.fullmatch(r"[A-Za-z\u0B80-\u0BFF .'-]+", name):
        return None, None, "Please enter your name (letters only, at least 2 characters)."
    if not re.fullmatch(r"[6-9]\d{9}", phone):
        return None, None, "Please enter a valid 10-digit mobile number (starts with 6, 7, 8 or 9)."
    return name, phone, None


def login_user(name, phone):
    """Create the user if new, otherwise update name/last login. Returns (user_dict, is_new)."""
    now = datetime.now().isoformat(timespec="seconds")
    with _conn() as c:
        row = c.execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
        if row is None:
            c.execute("INSERT INTO users VALUES (?,?,?,?)", (phone, name, now, now))
            is_new = True
        else:
            c.execute("UPDATE users SET name = ?, last_login = ? WHERE phone = ?", (name, now, phone))
            is_new = False
    return {"name": name, "phone": phone}, is_new


def save_prediction(phone, age, symptoms, top_result, probabilities):
    with _conn() as c:
        c.execute(
            "INSERT INTO predictions (phone, created_at, age, symptoms, top_result, probabilities) "
            "VALUES (?,?,?,?,?,?)",
            (phone, datetime.now().isoformat(timespec="seconds"), age,
             json.dumps(symptoms), top_result, json.dumps(probabilities)),
        )


def get_history(phone, limit=50):
    with _conn() as c:
        rows = c.execute(
            "SELECT * FROM predictions WHERE phone = ? ORDER BY id DESC LIMIT ?", (phone, limit)
        ).fetchall()
    return [dict(r) for r in rows]
