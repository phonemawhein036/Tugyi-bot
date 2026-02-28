import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        daily_count INTEGER DEFAULT 0,
        expiry_date TEXT,
        is_paid INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
