import sqlite3

# =========================
# INIT DATABASE
# =========================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score REAL,
        matched TEXT,
        missing TEXT
    )
    """)

    conn.commit()
    conn.close()

# =========================
# USER FUNCTIONS
# =========================
def add_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except:
        pass

    conn.close()

def check_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    data = c.fetchone()

    conn.close()
    return data

# =========================
# SAVE RESULT
# =========================
def save_result(username, score, matched, missing):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO results (username, score, matched, missing)
    VALUES (?, ?, ?, ?)
    """, (username, score, str(matched), str(missing)))

    conn.commit()
    conn.close()

# =========================
# HISTORY
# =========================
def get_history(username):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("SELECT score, matched, missing FROM results WHERE username=?", (username,))
    data = c.fetchall()

    conn.close()
    return data
