import sqlite3

conn = sqlite3.connect('sea-assignment/database.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    approved INTEGER DEFAULT 0,
    user_type TEXT NOT NULL
)""")

user_data = {'username': 'admin', 'password': '123', 'user_type': 'admin', 'approved': True}
c.execute('INSERT INTO users(username, password, user_type, approved) VALUES (?, ?, ?, ?)',
        (user_data['username'], user_data['password'], user_data['user_type'], user_data['approved']))


conn.commit()
conn.close()
