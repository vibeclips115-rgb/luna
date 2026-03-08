import sqlite3
import time

START_BALANCE = 1000

conn = sqlite3.connect("moonlight.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER,
    last_daily INTEGER DEFAULT 0
)
""")
conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS clans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    leader_id INTEGER,
    balance INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clan_members (
    user_id INTEGER UNIQUE,
    clan_id INTEGER,
    role TEXT
)
""")

# ---------------- STATISTICS TABLES ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_messages (
    user_id INTEGER PRIMARY KEY,
    count INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_voice (
    user_id INTEGER PRIMARY KEY,
    seconds INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mod_actions (
    user_id INTEGER PRIMARY KEY,
    kicks INTEGER DEFAULT 0,
    bans INTEGER DEFAULT 0
)
""")

conn.commit()

def get_balance(user_id: int) -> int:
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    if row is None:
        cursor.execute(
            "INSERT INTO users (user_id, balance, last_daily) VALUES (?, ?, ?)",
            (user_id, START_BALANCE, 0)
        )
        conn.commit()
        return START_BALANCE
    return row[0]

# ---------------- STATISTICS FUNCTIONS ----------------

def add_message(user_id: int):
    cursor.execute(
        "INSERT INTO user_messages (user_id, count) VALUES (?, 1) "
        "ON CONFLICT(user_id) DO UPDATE SET count = count + 1",
        (user_id,)
    )
    conn.commit()


def add_voice_time(user_id: int, seconds: int):
    cursor.execute(
        "INSERT INTO user_voice (user_id, seconds) VALUES (?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET seconds = seconds + ?",
        (user_id, seconds, seconds)
    )
    conn.commit()


def get_user_activity(user_id: int):
    cursor.execute(
        "SELECT count FROM user_messages WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    messages = row[0] if row else 0

    cursor.execute(
        "SELECT seconds FROM user_voice WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    voice = row[0] if row else 0

    return messages, voice


def get_message_leaderboard(limit=10):
    cursor.execute(
        "SELECT user_id, count FROM user_messages ORDER BY count DESC LIMIT ?",
        (limit,)
    )
    return cursor.fetchall()

def set_balance(user_id: int, amount: int):
    cursor.execute(
        "UPDATE users SET balance = ? WHERE user_id = ?",
        (amount, user_id)
    )
    conn.commit()

def get_top_balances(limit=10):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, balance FROM users ORDER BY balance DESC LIMIT ?",
        (limit,)
    )
    return cursor.fetchall()

def get_last_daily(user_id: int) -> int:
    cursor.execute("SELECT last_daily FROM users WHERE user_id = ?", (user_id,))
    return cursor.fetchone()[0]

def set_daily(user_id: int, timestamp: int) -> None:
    cursor.execute(
        "UPDATE users SET last_daily = ? WHERE user_id = ?",
        (timestamp, user_id)
    )
    conn.commit()
