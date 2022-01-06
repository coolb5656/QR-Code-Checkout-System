import sqlite3

c = sqlite3.connect("db/db.db")

with open("db/db_schema.sql", 'r') as sql_file:
    c.executescript(sql_file.read())

c.close()