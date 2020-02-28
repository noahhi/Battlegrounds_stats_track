import sqlite3 as sql

conn = sql.connect('database.db')

c = conn.cursor()

c.execute('''CREATE TABLE runs
                        (date text, hero text, place integer)''')

conn.commit()
conn.close()
