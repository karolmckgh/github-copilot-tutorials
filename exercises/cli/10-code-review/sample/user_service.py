"""A small user service with several deliberate problems.

This file is intentionally flawed so you can practice running and customizing
a Copilot code review. Do NOT use this code as a reference for real projects.
"""

import sqlite3

# Problem: hardcoded secret committed to source control
API_KEY = "sk_live_51H8xQ2eZvKYlo2C0hardcodedsecret"
DB_PATH = "users.db"


def get_user(user_id):
    # Problem: SQL injection via f-string interpolation
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    row = cursor.fetchone()
    # Problem: connection is never closed (resource leak)
    return row


def create_user(name, email, password):
    # Problem: no input validation on name/email/password
    # Problem: password stored in plain text
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO users (name, email, password) VALUES ('{name}', '{email}', '{password}')"
    )
    conn.commit()
    conn.close()
    return True


def find_admin(users):
    # Problem: comparison to None with == instead of 'is'
    for user in users:
        if user.get("role") == None:
            continue
        if user["role"] == "admin":
            return user
    return None


def divide_quota(total, num_users):
    # Problem: no guard against division by zero
    return total / num_users


def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        # Problem: bare except swallows all errors silently
        return None
