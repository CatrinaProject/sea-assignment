import sqlite3
import re
from flask import session


def register_user_to_db(username, password):  # Registers new users to the database as a 'non-approved' regular user
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    user_data = {'username': username, 'password': password, 'user_type': 'regular', 'approved': False}
    cur.execute('INSERT INTO users(username, password, user_type, approved) VALUES (?, ?, ?, ?)',
                (user_data['username'], user_data['password'], user_data['user_type'], user_data['approved']))
    con.commit()
    con.close()


def check_user(username, password):  # Checks whether the user exists in the database
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT username,password FROM users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False


def is_admin():  # Checks whether the user is an admin
    if 'username' in session:
        username = session['username']
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT user_type FROM users WHERE username = ?", (username,))
        user_type = cur.fetchone()
        con.close()
        if user_type and user_type[0] == 'admin':
            return True
    return False


def validate_bad_chars(params):
    # Validate input using regex to prevent inappropriate characters.
    # Although this is managed in front-end scripting it adds an extra layer of protection on the server side.

    # Server-side validation using regex, must not contain special characters
    if not re.match(r'^[a-zA-Z0-9\s\-.,\']+?$', params):
        return "Invalid characters or length detected.", 400

