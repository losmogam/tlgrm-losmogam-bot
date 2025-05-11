import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        telegram_id INTEGER PRIMARY KEY,
        active INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()

def set_user_active(telegram_id, active):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (telegram_id, active) VALUES (?, ?)", (telegram_id, active))
    conn.commit()
    conn.close()

def is_user_active(telegram_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT active FROM users WHERE telegram_id = ?", (telegram_id,))
    row = c.fetchone()
    conn.close()
    return row and row[0] == 1
