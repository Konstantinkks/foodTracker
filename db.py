import sqlite3
from datetime import datetime, timedelta

DB_NAME = "products.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            quantity TEXT,
            expiry TEXT
        )
        """)

def add_product(user_id, name, qty, expiry):
    try:
        datetime.strptime(expiry, "%Y-%m-%d")
    except ValueError:
        return False
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("INSERT INTO products (user_id, name, quantity, expiry) VALUES (?, ?, ?, ?)",
                     (user_id, name, qty, expiry))
    return True

def get_products(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT name, quantity, expiry FROM products WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

def get_expiring_products(within_days=2):
    today = datetime.now().date()
    deadline = today + timedelta(days=within_days)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute("SELECT user_id, name, expiry FROM products")
        result = {}
        for user_id, name, expiry in cursor.fetchall():
            try:
                exp_date = datetime.strptime(expiry, "%Y-%m-%d").date()
                if today <= exp_date <= deadline:
                    result.setdefault(user_id, []).append((name, expiry))
            except:
                continue
        return result