import sqlite3
from datetime import datetime

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            last_generated TEXT
        )
    """)

    conn.commit()
    conn.close()


def can_generate(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    today = datetime.utcnow().date().isoformat()

    c.execute("SELECT last_generated FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row:
        if row[0] == today:
            conn.close()
            return False
        else:
            c.execute("UPDATE users SET last_generated = ? WHERE user_id = ?", (today, user_id))
    else:
        c.execute("INSERT INTO users (user_id, last_generated) VALUES (?, ?)", (user_id, today))

    conn.commit()
    conn.close()
    return True
