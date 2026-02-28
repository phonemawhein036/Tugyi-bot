import sqlite3
from datetime import datetime, timedelta

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        daily_count INTEGER DEFAULT 0,
        last_generate TEXT,
        expiry_date TEXT,
        is_banned INTEGER DEFAULT 0,
        is_vip INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    data = cur.fetchone()
    conn.close()
    return data


def add_user(user_id, username):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?,?)",
                (user_id, username))
    conn.commit()
    conn.close()


def update_usage(user_id):
    now = datetime.now().isoformat()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        UPDATE users 
        SET daily_count = daily_count + 1,
            last_generate = ?
        WHERE user_id = ?
    """, (now, user_id))

    conn.commit()
    conn.close()


def reset_daily_if_needed(user_id):
    user = get_user(user_id)
    if not user:
        return

    last = user[3]
    if last:
        last_time = datetime.fromisoformat(last)
        if datetime.now() - last_time > timedelta(hours=24):
            conn = sqlite3.connect(DB)
            cur = conn.cursor()
            cur.execute("UPDATE users SET daily_count = 0 WHERE user_id=?", (user_id,))
            conn.commit()
            conn.close()
