import sqlite3

def init_db():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

def add_item(name, price):
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, price) VALUES (?, ?)", (name, price))
    conn.commit()
    conn.close()

def get_all_items():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM items")
    rows = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "price": row[1]} for row in rows]

def clear_ledger():
    conn = sqlite3.connect("ledger.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()