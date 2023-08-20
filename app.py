# app.py serves as the backend of the web application, handling routing, data processing,
# and interactions with the database to ensure the proper functioning of the application's features.

import re
import sqlite3

from flask import Flask, redirect, render_template, request, session


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


app = Flask(__name__)
app.secret_key = "ee3rs2"


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
    # Validate input using regex to prevent inappropriate characters
    valid_chars_pattern = re.compile(r'^[a-zA-Z0-9\s\-.,\']+?$')
    if not valid_chars_pattern.match(params) or len(params) > 50:
        return "Invalid characters or length detected."


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
def televisions():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM televisions")  # Get all the television records to be viewed on the page as a list
    television_results = cur.fetchall()
    con.commit()
    con.close()
    return render_template('televisions.html', television_results=television_results)


def extract_television_form_values(tv_request):
    return {
        'brand': tv_request.form['brand'],
        'audio': tv_request.form['audio'],
        'resolution': tv_request.form['resolution'],
        'refresh_rate': tv_request.form['refresh_rate'],
        'screen_size': tv_request.form['screen_size']
    }


@app.route('/televisions/add', methods=['POST'])  # Route to add a new television record
def add_television_record():
    if request.method == 'POST':
        form_values = extract_television_form_values(request)

        # Insert new television record with parameters submitted by the user
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Televisions (brand, audio, resolution, refresh_rate, screen_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (form_values['brand'], form_values['audio'], form_values['resolution'],
              form_values['refresh_rate'], form_values['screen_size']))
        conn.commit()
        conn.close()

        return redirect('/televisions')  # Redirect to the page displaying television records


@app.route('/tests', methods=['GET'])  # Route to display a list of tests
def tests():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    # Get all the test records to be viewed on the page as a list
    cur.execute("SELECT * FROM tests")
    test_cases = cur.fetchall()
    con.commit()
    con.close()
    return render_template('tests.html', test_cases=test_cases)


def extract_tests_form_values(test_request):
    return {
        'test_name': test_request.form['test_name'],
        'duration': test_request.form['duration'],
        'region': test_request.form['region'],
        'audio_test_type': test_request.form['audio_test_type'],
        'playback_type': test_request.form['playback_type'],
        'test_criteria': test_request.form['test_criteria'],
        'test_parameters': test_request.form['test_parameters']
    }


@app.route('/tests/add', methods=['POST'])  # Route to add a new test record
def add_test_record():
    if request.method == 'POST':
        form_values = extract_tests_form_values(request)

        # Insert new test record with parameters submitted by the user
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Tests (
                        test_name, duration, region, audio_test_type, playback_type, test_criteria, test_parameters
                        )
            VALUES (?, ?, ?, ?, ?, ?, ?) ''',
                    (form_values['test_name'], form_values['duration'], form_values['region'],
                     form_values['audio_test_type'], form_values['playback_type'], form_values['test_criteria'],
                     form_values['test_parameters']))
        conn.commit()
        conn.close()

        return redirect('/tests')  # Redirect to the page displaying television records


# ADMIN FUNCTIONALITY: The following admin/ routes will call the check_if_admin route. Only admins have permission.
@app.route('/admin/dashboard', methods=["GET", "POST"])  # Admin dashboard route: displays pending users and admin users
def admin_dashboard():
    if request.method == 'POST':
        selected_users = request.form.getlist('approve_user')
        if selected_users:
            con = sqlite3.connect('database.db')
            cur = con.cursor()

            for username in selected_users:
                # Update user_type to 'admin' and approved to 1 for the selected user(s)
                cur.execute('UPDATE users SET user_type = ?, approved = ? WHERE username = ?',
                            ('admin', 1, username))

            con.commit()
            con.close()
        else:
            print('No users selected for approval.')

    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_type = 'regular' AND approved = 0")  # Get all regular users
    pending_users = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE user_type = 'admin' AND approved = 1")  # Get all admin users
    admins = cur.fetchall()

    con.close()

    return render_template('admin-dashboard.html', pending_users=pending_users, admins=admins)


@app.route('/admin/televisions/edit', methods=['GET'])  # Route to load the 'edit a television record' page
def edit_television():
    tv_id = request.args.get('tv_id')
    # Get the requested television record with the user requested tv_id
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Televisions WHERE tv_id = ?", (tv_id,))
    tv_record = cur.fetchone()
    conn.close()
    return render_template('edit-televisions.html', tv_id=tv_id, brand=tv_record[1], audio=tv_record[2],
                           resolution=tv_record[3], refresh_rate=tv_record[4], screen_size=tv_record[5])


@app.route('/admin/televisions/edit/submit', methods=['POST'])  # Route to edit a television record
def update_television_record():
    if request.method == 'POST':
        form_values = extract_television_form_values(request)

        validate_bad_chars(params=form_values['brand'] + form_values['audio'] +
                                  form_values['resolution'] + form_values['refresh_rate'] +
                                  form_values['screen_size'])

        # Update the television record
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            UPDATE Televisions
            SET brand=?, audio=?, resolution=?, refresh_rate=?, screen_size=?
            WHERE tv_id=?
        ''', (form_values['brand'], form_values['audio'], form_values['resolution'],
              form_values['refresh_rate'], form_values['screen_size'], request.form['tv_id']))
        conn.commit()
        conn.close()

        return redirect('/televisions')  # Redirect to the page displaying television records


@app.route('/admin/televisions/delete', methods=['GET'])  # Route to delete a television record
def delete_television():
    tv_id = request.args.get('tv_id')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Televisions WHERE tv_id = ?", (tv_id,))
    conn.commit()
    conn.close()
    return redirect('/televisions')


@app.route('/admin/tests/edit', methods=['GET'])  # Route to load the 'edit a test record' page
def edit_tests():
    test_id = request.args.get('test_id')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tests WHERE test_id = ?", (test_id,))
    test_record = cur.fetchone()
    conn.close()
    return render_template('edit-tests.html', test_id=test_id, test_name=test_record[1], duration=test_record[2],
                           region=test_record[3], audio_test_type=test_record[4], playback_type=test_record[5],
                           test_criteria=test_record[6], test_parameters=test_record[7])


@app.route('/admin/tests/edit/submit', methods=['POST'])  # Route to edit a test record
def update_test_record():
    is_admin()
    if request.method == 'POST':
        form_values = extract_tests_form_values(request)

        validate_bad_chars(
            params=form_values['test_name'] + form_values['duration'] + form_values['region']
                   + form_values['audio_test_type'] + form_values['playback_type'] + form_values['test_criteria']
                   + form_values['test_parameters'])

        # Validate duration as a decimal with up to 2 decimal places and a total of 5 digits
        if not re.match(r'^\d{1,5}(\.\d{1,2})?$', form_values['duration']):
            return "Invalid duration value."

        # Update the test record
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            UPDATE Tests
            SET test_name=?, duration=?, region=?, audio_test_type=?, playback_type=?, test_criteria=?, 
            test_parameters=? WHERE test_id=? 
            ''', (form_values['test_name'], form_values['duration'], form_values['region'],
                  form_values['audio_test_type'], form_values['playback_type'], form_values['test_criteria'],
                  form_values['test_parameters'], request.form['test_id']))
        conn.commit()
        conn.close()
        return redirect('/tests')  # Redirect to the page displaying test records


@app.route('/admin/tests/delete', methods=['GET'])  # Route to delete a test record
def delete_test():
    test_id = request.args.get('test_id')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Tests WHERE test_id = ?", (test_id,))
    conn.commit()
    conn.close()
    return redirect('/tests')


@app.route('/logout')  # Logout route: logs the user out by clearing session
def logout():
    session['username'] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
