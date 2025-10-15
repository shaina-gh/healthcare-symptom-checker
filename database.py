# database.py
import sqlite3
import json
from datetime import datetime

DATABASE_NAME = "symptom_checker.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # This allows accessing columns by name
    return conn

def init_db():
    """Initializes the database table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS symptom_checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symptoms TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_check(symptoms: str, response: dict):
    """Saves a symptom check interaction to the database."""
    conn = get_db_connection()
    # SQLite doesn't have a JSON type, so we store the response as a text string
    response_str = json.dumps(response)
    conn.execute(
        "INSERT INTO symptom_checks (symptoms, response) VALUES (?, ?)",
        (symptoms, response_str)
    )
    conn.commit()
    conn.close()

def get_all_checks():
    """Retrieves all historical checks, ordered by most recent."""
    conn = get_db_connection()
    cursor = conn.execute("SELECT id, symptoms, response, created_at FROM symptom_checks ORDER BY created_at DESC")
    checks = [
        {
            "id": row["id"],
            "symptoms": row["symptoms"],
            "response": row["response"], # The response is a JSON string
            "created_at": row["created_at"]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return checks