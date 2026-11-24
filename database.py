import sqlite3

def get_connection(db_name="fraud.db"):
    return sqlite3.connect(db_name)

def init_db(db_name="fraud.db"):
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS CARDS (
        token TEXT PRIMARY KEY,
        holder TEXT,
        bank TEXT,
        credit_limit REAL,
        status TEXT
    );
    CREATE TABLE IF NOT EXISTS ALERTS (
        alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT,
        amount REAL,
        device_hash TEXT,
        risk_score INTEGER,
        decision TEXT,
        status TEXT,
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS SHARED_THREATS (
        device_hash TEXT PRIMARY KEY,
        reported_by_bank TEXT
    );
    """)

    cur.execute("SELECT COUNT(*) FROM CARDS")
    if cur.fetchone()[0] == 0:
        cur.executemany("INSERT INTO CARDS VALUES (?, ?, ?, ?, ?)", [
            ("TOK_101", "Aarav Sharma", "HDFC Bank", 100000.0, "Active"),
            ("TOK_102", "Sneha Reddy", "ICICI Bank", 60000.0, "Active"),
        ])
    conn.commit()
    conn.close()
