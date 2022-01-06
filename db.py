import sqlite3

def connect():
    conn = sqlite3.connect('db/db.db')
    conn.row_factory = sqlite3.Row
    return conn