import sqlite3
import re
from flask import session, flash, redirect, request


def register_user_to_db(username, password):  # Registers new users to the database as a 'non-approved' regular user
    con = sqlite3.connect('database.db')
    cur = con.cursor()  # Connect to the database and insert a new record with username and password provided
    user_data = {'username': username, 'password': password, 'user_type': 'regular', 'approved': False}
    cur.execute('INSERT INTO users(username, password, user_type, approved) VALUES (?, ?, ?, ?)',
                (user_data['username'], user_data['password'], user_data['user_type'], user_data['approved']))
    con.commit()
    con.close()


def check_user(username, password):  # Checks whether the username and password exists in the database
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT username,password FROM users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:  # If username/password exists, then sqlite will return True, else False
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
        if user_type and user_type[0] == 'admin':  # If the user_type is an admin, return True, else False
            return True
    return False


def validate_bad_chars(params):
    # Validate input using regex to prevent inappropriate characters.
    # Although this is managed in front-end scripting it adds an extra layer of protection on the server side.

    # Server-side validation using regex, must not contain special characters
    if not re.match(r'^[a-zA-Z0-9\s\-.,\']+?$', params):
        return "Invalid characters or length detected.", 400


def validate_decimal(duration):
    # Validate duration as a decimal with up to 2 decimal places and a total of 5 digits
    # Although this is managed in front-end scripting it adds an extra layer of protection on the server side.
    if not re.match(r'^\d{1,5}(\.\d{1,2})?$', duration):
        return "Invalid duration value.", 400
