# app.py serves as the backend of the web application, handling routing, data processing,
# and interactions with the database to ensure the proper functioning of the application's features.

from datetime import timedelta
from flask import Flask, redirect, render_template, request, session, flash
from logger.create_logger import create_logger
from helpers import hash_password, register_user_to_db, check_user, is_admin, clean_ip_address, validate_username, validate_password
from televisions import televisions, add_television_record, edit_television, update_television_record, delete_television
from tests import tests, add_test_record, edit_tests, update_test_record, delete_test
from admin_dashboard import admin_dashboard

app = Flask(__name__)
app.secret_key = "ee3rs2"
app.permanent_session_lifetime = timedelta(minutes=60)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

logger = create_logger()


@app.before_request  # Before a each request, check whether the page is a /admin route
def check_admin_route():
    if request.path.startswith('/admin'):  # If /admin routes are clicked on the check_if_admin route.        
        if not is_admin():  # If the session username is not an admin, flash the error message and redirect to home page
            flash("Sorry, you must be an admin to perform this action. Please contact an admin.", "error")
            return redirect("/home")
        
        if 'ip_address' in session:
            current_ip_address = clean_ip_address(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
            # Check if the IP address in the session matches the current IP address. If not, redirect to login page.
            if session['ip_address'] != current_ip_address:
                flash("Sorry, you must login again. Your IP address has changed.", "error")
                return redirect("/")
        else:
            flash("Sorry, you must login again. No IP address found. ", "error")
            return redirect("/")

@app.route("/")  # Main route: renders the login page
def index():
    logger.info('Processing login page')
    return render_template('login.html')  # Renders the login page


@app.route('/register', methods=["POST", "GET"])  # Route for user registration
def register():
    if request.method == 'POST':  # When a "submit" (POST) request is made on the /register page
        username = request.form['username']  # Get the username and password
        password = request.form['password']

        if validate_username(username) or validate_password(password):
            return redirect("/")
                
        hashed_password = hash_password(password)

        register_user_to_db(username, hashed_password)  # Call register user to database with the username and hashed password
        logger.info("Registered a new user to the database")
        return redirect("/")  # redirect to the login page
    else:
        return render_template('register.html')  # render the registration page


@app.route('/login', methods=["POST", "GET"])  # Route for user login
def login():
    if request.method == 'POST':   # When a "submit" (POST) request is made on the /login page
        username = request.form['username']  # Get the username and password
        password = request.form['password']

        if validate_username(username) or validate_password(password):
            return redirect("/")

        if check_user(username, password):  # Creates a new session for the user, then redirects them to the home page
            session['username'] = username  # Add username to the session
            session['ip_address'] = clean_ip_address(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)) # Add IP address to the session
            logger.info('Login succeeded, processing home page')
            return redirect("/home")  # Go to the home page
        else:
            message = f'Could not login user: {username}, as username or password was invalid, redirecting to login failed page'
            logger.error(message)
            flash(message, "error")
            return render_template('login-failed.html')  # Go to login-failed page when their user doesn't exist
    else:
        return redirect("/")


@app.route('/home', methods=['POST', "GET"])  # Home route: displays the user's home page after logging in
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        message = "User not in session, redirecting to login failed page"
        logger.error(message)
        flash(message, "error")
        return render_template('login-failed.html')


@app.route('/televisions', methods=['GET'])  # Route to display a list of televisions
def televisions_route():
    logger.info('Processing televisions page')
    return televisions()


@app.route('/televisions/add', methods=['POST'])  # Route to add a new television record
def televisions_add_roue():
    logger.info('Adding a new television record')
    return add_television_record()


@app.route('/televisions/edit', methods=['GET'])  # Route to load the 'edit a television record' page
def televisions_edit_route():
    logger.info('Editing a television record')
    return edit_television()


@app.route('/televisions/edit/submit', methods=['POST'])  # Route to edit a television record
def televisions_edit_submit_route():
    logger.info('Updating a television record')
    return update_television_record()


@app.route('/admin/televisions/delete', methods=['GET'])  # Route to delete a television record
def television_delete_route():
    logger.info('Deleting a television record')
    return delete_television()


@app.route('/tests', methods=['GET'])  # Route to display a list of tests
def tests_route():
    logger.info('Processing tests page')
    return tests()


@app.route('/tests/add', methods=['POST'])  # Route to add a new test record
def tests_add_route():
    logger.info('Adding a new test record')
    return add_test_record()


@app.route('/tests/edit', methods=['GET'])  # Route to load the 'edit a test record' page
def tests_edit_route():
    logger.info('Editing a test record')
    return edit_tests()


@app.route('/tests/edit/submit', methods=['POST'])  # Route to edit a test record
def tests_edit_submit_route():
    logger.info('Updating a test record')
    return update_test_record()


@app.route('/admin/tests/delete', methods=['GET'])  # Route to delete a test record
def test_delete_route():
    logger.info('Deleting a test record')
    return delete_test()


@app.route('/admin/dashboard', methods=["GET", "POST"])  # Admin dashboard route: displays pending users and admin users
def admin_approval_dashboard_route():
    logger.info('Processing admin dashboard')
    return admin_dashboard()


@app.route('/logout')  # Logout route: logs the user out by clearing session
def logout():
    session.clear()
    logger.info('Session is cleared, logging the user out')
    return redirect("/")  # Redirect to the login page


if __name__ == '__main__':
    app.run(debug=True)
