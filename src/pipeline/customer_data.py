import sqlite3
from src.pipeline.utils import create_connection

def create_customer_table():
    conn = create_connection()
    query = """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        dob TEXT,
        phone TEXT,
        joining_date TEXT,
        enrollment_date TEXT NOT NULL,
        points INTEGER DEFAULT 0
    )
    """
    conn.execute(query)
    conn.commit()
    conn.close()

def add_customer(name, dob, phone, joining_date, points):
    conn = create_connection()
    query = "INSERT INTO customers (name, dob, phone, joining_date, points) VALUES (?, ?, ?, ?, ?)"
    conn.execute(query, (name, dob, phone, joining_date, points))
    conn.commit()
    conn.close()

def search_customer(name):
    conn = create_connection()
    query = "SELECT * FROM customers WHERE name = ?"
    cursor = conn.execute(query, (name,))
    result = cursor.fetchone()
    conn.close()
    return result

def delete_customer(name):
    conn = create_connection()
    query = "DELETE FROM customers WHERE name = ?"
    conn.execute(query, (name,))
    conn.commit()
    conn.close()

def update_points(name, points):
    conn = create_connection()
    query = "UPDATE customers SET points = points + ? WHERE name = ?"
    conn.execute(query, (points, name))
    conn.commit()
    conn.close()
