import sqlite3

conn = sqlite3.connect("books.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_reads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book TEXT
)
""")

conn.commit()