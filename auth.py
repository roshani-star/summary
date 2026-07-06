import sqlite3

conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()

# ---------- CREATE TABLE ----------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.commit()

# ---------- REGISTER ----------

def register_user(username, password):

    cursor.execute(
        """
        INSERT INTO users(username, password)
        VALUES(?, ?)
        """,
        (username, password)
    )

    conn.commit()

    return True

# ---------- LOGIN ----------

def login_user(username, password):

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username=? AND password=?
        """,
        (username, password)
    )

    data = cursor.fetchone()

    return data