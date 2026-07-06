import sqlite3

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    trial_count INTEGER DEFAULT 3,
    is_premium INTEGER DEFAULT 0
)
""")

conn.commit()

print("Database Created Successfully")