import sqlite3

conn = sqlite3.connect('sea-assignment/database.db')

c = conn.cursor()

c.execute("""CREATE TABLE users(
        id integer,
        username Text not null,
        password TEXT not null,
        PRIMARY KEY(id)
        )""")
conn.commit()

conn.close()