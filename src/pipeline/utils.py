import sqlite3

def create_connection():
    conn = sqlite3.connect("customers.db")  # Database file
    return conn
