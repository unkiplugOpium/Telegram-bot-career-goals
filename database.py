import sqlite3 

def connect():
    return sqlite3.connect("person_career.db")

def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        age INTEGER,
        interests TEXT,
        goal TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        skills TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_user(user_id, age, interests, goal):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO users VALUES (?, ?, ?, ?)",
        (user_id, age, interests, goal)
    )
    conn.commit()
    conn.close()
