# app.py serves as the backend of the web application, handling routing, data processing,
# and interactions with the database to ensure the proper functioning of the application's features.

import re
from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, flash, url_for
from helpers import hash_password, register_user_to_db, check_user, is_admin
from televisions import televisions, add_television_record, edit_television, update_television_record, delete_television
from tests import tests, add_test_record, edit_tests, update_test_record, delete_test
from admin_dashboard import admin_dashboard

app = Flask(__name__)
app.secret_key = "ee3rs2"
app.permanent_session_lifetime = timedelta(minutes=60)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True



@app.before_request  # Before a each request, check whether the page is a /admin route
def check_admin_route():
    if request.path.startswith('/admin'):  # If /admin routes are clicked on the check_if_admin route.
        if not is_admin():  # If the session username is not an admin, flash the error message and redirect to home page
            flash("Sorry, you must be an admin to perform this action. Please contact an admin.", "error")
            return redirect("/home")

@app.before_request
def check_session_timeout():
    # Exclude the login route from session timeout check
    if request.endpoint == 'login':
        return

    # When session times out, redirect the next request to the login page
    if 'username' not in session:
        return redirect(url_for('login'))


@app.route("/")  # Main route: renders the login page
def index():
    return render_template('login.html')  # Renders the login page


@app.route('/register', methods=["POST", "GET"])  # Route for user registration
def register():
    if request.method == 'POST':  # When a "submit" (POST) request is made on the /register page
        username = request.form['username']  # Get the username and password
        password = request.form['password']

        # Server-side validation for username using regex, must be alphabetical and less than 50 characters
        if not re.match(r"^[a-zA-Z]{5,}$", username):
            return "Invalid username. Must meet the specified criteria.", 400

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
            return "Invalid password. Must meet the specified criteria.", 400
        
        hashed_password = hash_password(password)

        register_user_to_db(username, hashed_password)  # Call register user to database with the username and hashed password
        return redirect("/")  # redirect to the login page
    else:
        return render_template('register.html')  # render the registration page


@app.route('/login', methods=["POST", "GET"])  # Route for user login
def login():
    if request.method == 'POST':   # When a "submit" (POST) request is made on the /login page
        username = request.form['username']  # Get the username and password
        password = request.form['password']
        if check_user(username, password):  # Creates a new session for the user, then redirects them to the home page
            session['username'] = username  # Add username to the session
            return redirect("/home")  # Go to the home page
        else:
            return render_template('login-failed.html')  # Go to login-failed page when their user doesn't exist
    else:
        return redirect("/")


@app.route('/home', methods=['POST', "GET"])  # Home route: displays the user's home page after logging in
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('login-failed.html')


@app.route('/televisions', methods=['GET'])  # Route to display a list of televisions
def televisions_route():
    return televisions()


@app.route('/televisions/add', methods=['POST'])  # Route to add a new television record
def televisions_add_roue():
    return add_television_record()


@app.route('/televisions/edit', methods=['GET'])  # Route to load the 'edit a television record' page
def televisions_edit_route():
    return edit_television()


@app.route('/televisions/edit/submit', methods=['POST'])  # Route to edit a television record
def televisions_edit_submit_route():
    return update_television_record()


@app.route('/admin/televisions/delete', methods=['GET'])  # Route to delete a television record
def television_delete_route():
    return delete_television()


@app.route('/tests', methods=['GET'])  # Route to display a list of tests
def tests_route():
    return tests()


@app.route('/tests/add', methods=['POST'])  # Route to add a new test record
def tests_add_route():
    return add_test_record()


@app.route('/tests/edit', methods=['GET'])  # Route to load the 'edit a test record' page
def tests_edit_route():
    return edit_tests()


@app.route('/tests/edit/submit', methods=['POST'])  # Route to edit a test record
def tests_edit_submit_route():
    return update_test_record()


@app.route('/admin/tests/delete', methods=['GET'])  # Route to delete a test record
def test_delete_route():
    return delete_test()


@app.route('/admin/dashboard', methods=["GET", "POST"])  # Admin dashboard route: displays pending users and admin users
def admin_approval_dashboard_route():
    return admin_dashboard()


@app.route('/logout')  # Logout route: logs the user out by clearing session
def logout():
    session.clear()
    return redirect("/")  # Redirect to the login page


if __name__ == '__main__':
    app.run(debug=True)
