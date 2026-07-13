import sqlite3

conn = sqlite3.connect("shield_ai.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    company TEXT,
    email TEXT,
    website TEXT,
    prediction TEXT,
    trust_score INTEGER
)
""")

conn.commit()

conn.close()

print("Database Created Successfully")