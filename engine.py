import hashlib
from datetime import datetime
from database import get_connection

def hash_device(device_id):
    """Anonymizes device ID using SHA-256 before cross-bank sharing."""
    return hashlib.sha256(device_id.encode()).hexdigest()[:16]

def score_transaction(token, amount, device_id, db_name="fraud.db"):
    conn = get_connection(db_name)
    cur = conn.cursor()

    cur.execute("SELECT bank, credit_limit, status FROM CARDS WHERE token = ?", (token,))
    card = cur.fetchone()
    if not card:
        conn.close()
        raise ValueError("Invalid card token.")

    bank, limit, status = card
    if status == "Blocked":
        conn.close()
        return 100, "Decline", "Card is already blocked"

    dev_hash = hash_device(device_id)
    score = 0
    reasons = []

    if amount > limit:
        score += 70
        reasons.append("Exceeds credit limit")
    elif amount >= limit * 0.8:
        score += 45
        reasons.append("High utilization (>80%)")

    cur.execute("SELECT reported_by_bank FROM SHARED_THREATS WHERE device_hash = ?", (dev_hash,))
    threat = cur.fetchone()
    if threat:
        score += 55
        reasons.append(f"Device flagged by {threat[0]}")

    score = min(score, 100)

    if score >= 70:
        decision = "Decline"
        cur.execute("UPDATE CARDS SET status = 'Blocked' WHERE token = ?", (token,))
    elif score >= 40:
        decision = "Verify"
    else:
        decision = "Approve"

    if decision in ("Decline", "Verify"):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            INSERT INTO ALERTS (token, amount, device_hash, risk_score, decision, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'Open', ?)
        """, (token, amount, dev_hash, score, decision, now))

    conn.commit()
    conn.close()
    return score, decision, ", ".join(reasons) if reasons else "Normal transaction"

def resolve_alert(alert_id, is_fraud, db_name="fraud.db"):
    conn = get_connection(db_name)
    cur = conn.cursor()

    cur.execute("SELECT token, device_hash FROM ALERTS WHERE alert_id = ? AND status = 'Open'", (alert_id,))
    alert = cur.fetchone()
    if not alert:
        conn.close()
        raise ValueError("Open Alert ID not found.")

    token, dev_hash = alert
    cur.execute("SELECT bank FROM CARDS WHERE token = ?", (token,))
    bank = cur.fetchone()[0]

    if is_fraud:
        cur.execute("UPDATE ALERTS SET status = 'Confirmed Fraud' WHERE alert_id = ?", (alert_id,))
        cur.execute("UPDATE CARDS SET status = 'Blocked' WHERE token = ?", (token,))
        cur.execute("INSERT OR IGNORE INTO SHARED_THREATS VALUES (?, ?)", (dev_hash, bank))
    else:
        cur.execute("UPDATE ALERTS SET status = 'False Positive' WHERE alert_id = ?", (alert_id,))
        cur.execute("UPDATE CARDS SET status = 'Active' WHERE token = ?", (token,))

    conn.commit()
    conn.close()

def get_all_alerts(db_name="fraud.db"):
    conn = get_connection(db_name)
    cur = conn.cursor()
    cur.execute("SELECT alert_id, token, amount, risk_score, decision, status FROM ALERTS")
    rows = cur.fetchall()
    conn.close()
    return rows
