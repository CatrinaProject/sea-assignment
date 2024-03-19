import sqlite3
import re
from logger.create_logger import create_logger
from flask import session, flash
from werkzeug.security import generate_password_hash, check_password_hash

logger = create_logger()

def clean_ip_address(ip_addresses_from_environment):
    ip_address = str(ip_addresses_from_environment.split(', ')[0].strip())
    dot_index = ip_address.rfind('.')
    
    if dot_index != -1:
        ip_address = ip_address[:dot_index]
    
    return ip_address

def register_user_to_db(username, hashed_password):  # Registers new users to the database as a 'non-approved' regular user
    con = sqlite3.connect('database.db')
    cur = con.cursor()  # Connect to the database and insert a new record with username and password provided
    user_data = {'username': username, 'password': hashed_password, 'is_admin': False}
    cur.execute('INSERT INTO users(username, password, is_admin) VALUES (?, ?, ?)',
                (user_data['username'], user_data['password'], user_data['is_admin']))
    con.commit()
    con.close()


def check_user(username, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    # Fetch the hashed password for the given username
    cur.execute('SELECT password FROM users WHERE username=?', (username,))
    stored_hashed_password = cur.fetchone()

    if stored_hashed_password:
        # Check if the entered password matches the stored hashed password
        password_match = check_password_hash(stored_hashed_password[0], password)

        if password_match:
            return True
        else:
            logger.error("Password entered by user: %s was incorrect", username)
            return False
    else:
        logger.error("Username: %s does not exist", username)
        return False


def is_admin():  # Checks whether the user is an admin
    if 'username' in session:
        username = session['username']
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
        user_type = cur.fetchone()
        con.close()
        if user_type and user_type[0] == 1 :  # If the user_type is an admin, return True, else False
            return True
    return False


def validate_username(username):
    # Server-side validation for username using regex, must be alphabetical and less than 50 characters
    if not re.match(r"^[a-zA-Z]{5,}$", username):
        message = "User input failed to pass Username regex validation"
        logger.error(message)
        flash(message, "error")
        return "Invalid username. Must meet the specified criteria.", 400


def validate_password(password):
    # Server-side validation for password using regex
    length_regex = r".{5,}"
    uppercase_regex = r"[A-Z]"
    lowercase_regex = r"[a-z]"
    digit_regex = r"\d"
    special_char_regex = r"[!@#$%^&*()_+{}\[\]:;<>,.?~\-]"

    is_length_valid = re.search(length_regex, password)
    is_uppercase_valid = re.search(uppercase_regex, password)
    is_lowercase_valid = re.search(lowercase_regex, password)
    is_digit_valid = re.search(digit_regex, password)
    is_special_char_valid = re.search(special_char_regex, password)

    # Check if all requirements are met
    if not (
            is_length_valid and
            is_uppercase_valid and
            is_lowercase_valid and
            is_digit_valid and
            is_special_char_valid
    ):
        message = "User input failed to pass Password regex validation"
        logger.error(message)
        flash(message, "error")
        return "Invalid password. Must meet the specified criteria.", 400


def validate_bad_chars(params):
    # Validate input using regex to prevent inappropriate characters.
    # Although this is managed in front-end scripting it adds an extra layer of protection on the server side.

    # Server-side validation using regex, must not contain special characters
    if not re.match(r'^[a-zA-Z0-9\s\-.,\']+?$', params):
        message = "User input failed to pass regex validation"
        logger.error(message)
        flash(message, "error")
        return "Invalid characters or length detected.", 400


def validate_decimal(duration):
    # Validate duration as a decimal with up to 2 decimal places and a total of 5 digits
    # Although this is managed in front-end scripting it adds an extra layer of protection on the server side.
    if not re.match(r'^\d{1,5}(\.\d{1,2})?$', duration):
        message = "User input failed to pass Decimal regex validation"
        logger.error(message)
        flash(message, "error")
        return "Invalid duration value.", 400


def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)