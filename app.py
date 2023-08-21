# app.py serves as the backend of the web application, handling routing, data processing,
# and interactions with the database to ensure the proper functioning of the application's features.

from flask import Flask, redirect, render_template, request, session
from helpers import register_user_to_db, check_user, is_admin
from televisions import televisions, add_television_record, edit_television, update_television_record, delete_television
from tests import tests, add_test_record, edit_tests, update_test_record, delete_test
from admin_dashboard import admin_dashboard


app = Flask(__name__)
app.secret_key = "ee3rs2"


@app.before_request  # Before each request, check if the user is an admin when accessing a /admin route
def check_admin_route():
    if request.path.startswith('/admin'):
        if not is_admin():
            session['error_banner'] = "Sorry, you must be an admin to perform this action. Please contact an admin."
            return redirect("/home")


@app.route("/")  # Main route: renders the login page
def index():
    return render_template('login.html')  # Renders the login page


@app.route('/register', methods=["POST", "GET"])  # Route for user registration
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)  # Registers the new user then redirects to login page
        return redirect("/")

    else:
        return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])  # Route for user login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):  # Creates a new session for the user, then redirects them to the home page
            session['username'] = username
            return redirect("/home")
        else:
            return render_template('login-failed.html')
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


@app.route('/tests', methods=['GET'])  # Route to display a list of tests
def tests_route():
    return tests()


@app.route('/tests/add', methods=['POST'])  # Route to add a new test record
def tests_add_route():
    return add_test_record()


# ADMIN FUNCTIONALITY: The following admin/ routes will call the check_if_admin route. Only admins have permission.
@app.route('/admin/dashboard', methods=["GET", "POST"])  # Admin dashboard route: displays pending users and admin users
def admin_approval_dashboard_route():
    return admin_dashboard()


@app.route('/admin/televisions/edit', methods=['GET'])  # Route to load the 'edit a television record' page
def televisions_edit_route():
    return edit_television()


@app.route('/admin/televisions/edit/submit', methods=['POST'])  # Route to edit a television record
def televisions_edit_submit_route():
    return update_television_record()


@app.route('/admin/televisions/delete', methods=['GET'])  # Route to delete a television record
def television_delete_route():
    return delete_television()


@app.route('/tests/edit', methods=['GET'])  # Route to load the 'edit a test record' page
def tests_edit_route():
    return edit_tests()


@app.route('/tests/edit/submit', methods=['POST'])  # Route to edit a test record
def tests_edit_submit_route():
    return update_test_record()


@app.route('/admin/tests/delete', methods=['GET'])  # Route to delete a test record
def test_delete_route():
    return delete_test()


@app.route('/logout')  # Logout route: logs the user out by clearing session
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
