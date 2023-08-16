import re
import sqlite3

from flask import Flask, redirect, render_template, request, session


def register_user_to_db(username, password):
    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    user_data = {'username': username, 'password': password, 'user_type': 'regular', 'approved': False}
    cur.execute('INSERT INTO users(username, password, user_type, approved) VALUES (?, ?, ?, ?)',
            (user_data['username'], user_data['password'], user_data['user_type'], user_data['approved']))
    con.commit()
    con.close()


def check_user(username, password):
    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    cur.execute('SELECT username,password FROM users WHERE username=? and password=?', (username, password))

    result = cur.fetchone()
    if result:
        return True
    else:
        return False


app = Flask(__name__)
app.secret_key = "weewoo"

def is_admin():
    if 'username' in session:
        username = session['username']
        con = sqlite3.connect('sea-assignment/database.db')
        cur = con.cursor()
        cur.execute("SELECT user_type FROM users WHERE username = ?", (username,))
        user_type = cur.fetchone()
        con.close()
        if user_type and user_type[0] == 'admin':
            return True
    return False

@app.before_request
def check_admin_route():
    if request.path.startswith('/admin'):
        if not is_admin():
            return redirect('/home')

@app.route("/")
def index():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        register_user_to_db(username, password)
        return redirect("/")

    else:
        return render_template('register.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(check_user(username, password))
        if check_user(username, password):
            session['username'] = username
            return redirect("/home")
        else:
            return render_template('login-failed.html')
    else:
        return redirect("/")


@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    else:
        return render_template('login-failed.html')
    
@app.route('/televisions', methods=['GET'])
def televisions():
    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM televisions")
    television_results = cur.fetchall()
    con.commit()
    con.close()
    return render_template('televisions.html', television_results=television_results)

@app.route('/tests', methods=['GET'])
def tests():
    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM tests")
    test_cases = cur.fetchall()
    con.commit()
    con.close()
    return render_template('tests.html', test_cases=test_cases)

@app.route('/admin/dashboard', methods=["GET", "POST"])
def admin_dashboard():
    if request.method == 'POST':
        selected_users = request.form.getlist('approve_user')
        if selected_users:
            con = sqlite3.connect('sea-assignment/database.db')
            cur = con.cursor()

            for username in selected_users:
                # Update user_type to 'admin' and approved to 1 for the selected user(s)
                cur.execute('UPDATE users SET user_type = ?, approved = ? WHERE username = ?',
                            ('admin', 1, username))

            con.commit()
            con.close()
        else:
            print('No users selected for approval.')

    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_type = 'regular' AND approved = 0")
    pending_users = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE user_type = 'admin' AND approved = 1")
    admins = cur.fetchall()

    con.close()

    return render_template('admin-dashboard.html', pending_users=pending_users, admins=admins)


@app.route('/admin/televisions/edit', methods=['GET'])
def edit_television():
    tv_id = request.args.get('tv_id')
    conn = sqlite3.connect('sea-assignment/database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Televisions WHERE tv_id = ?", (tv_id,))
    tv_record = cur.fetchone()
    conn.close()
    return render_template('edit-televisions.html', tv_id=tv_id, brand=tv_record[1], audio=tv_record[2], resolution=tv_record[3], refresh_rate=tv_record[4], screen_size=tv_record[5])

@app.route('/admin/televisions/edit/submit', methods=['POST'])
def update_television_record():
    if request.method == 'POST':
        tv_id = request.form['tv_id']
        brand = request.form['brand']
        audio = request.form['audio']
        resolution = request.form['resolution']
        refresh_rate = request.form['refresh_rate']
        screen_size = request.form['screen_size']

        # Validate input using regex to prevent inappropriate characters
        valid_chars_pattern = re.compile(r'^[a-zA-Z0-9\s\-.,\']+?$') 
        if not valid_chars_pattern.match(brand + audio + resolution + refresh_rate + screen_size) or len(brand + audio + resolution + refresh_rate + screen_size) > 50:
            return "Invalid characters or length detected."

        # Update the television record
        conn = sqlite3.connect('sea-assignment/database.db')
        cur = conn.cursor()
        cur.execute('''
            UPDATE Televisions
            SET brand=?, audio=?, resolution=?, refresh_rate=?, screen_size=?
            WHERE tv_id=?
        ''', (brand, audio, resolution, refresh_rate, screen_size, tv_id))
        conn.commit()
        conn.close()

        return redirect('/televisions')  # Redirect to the page displaying television records
    
@app.route('/admin/televisions/delete', methods=['GET'])
def delete_television():
    tv_id = request.args.get('tv_id')
    conn = sqlite3.connect('sea-assignment/database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Televisions WHERE tv_id = ?", (tv_id,))
    conn.commit()
    conn.close()
    return redirect('/televisions')

@app.route('/admin/tests/edit', methods=['GET'])
def edit_tests():
    test_id = request.args.get('test_id')
    conn = sqlite3.connect('sea-assignment/database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tests WHERE test_id = ?", (test_id,))
    test_record = cur.fetchone()
    conn.close()
    return render_template('edit-tests.html', test_id=test_id, test_name=test_record[1], duration=test_record[2], region=test_record[3], audio_test_type=test_record[4], playback_type=test_record[5], test_criteria=test_record[6], test_parameters=test_record[7])

@app.route('/admin/tests/edit/submit', methods=['POST'])
def update_test_record():
    is_admin()
    if request.method == 'POST':
        test_id = request.form['test_id']
        test_name = request.form['test_name']
        duration = request.form['duration']
        region = request.form['region']
        audio_test_type = request.form['audio_test_type']
        playback_type = request.form['playback_type']
        test_criteria = request.form['test_criteria']
        test_parameters = request.form['test_parameters']

        # Validate input using regex to prevent inappropriate characters
        valid_chars_pattern = re.compile(r'^[a-zA-Z0-9\s\-.,\']+?$') 
        if not valid_chars_pattern.match(test_name + duration + region + audio_test_type + playback_type + test_criteria + test_parameters) or len(test_name + duration + region + audio_test_type + playback_type + test_criteria + test_parameters) > 50:
            return "Invalid characters or length detected."
        else:
            print("huh")

        # Validate duration as a decimal with up to 2 decimal places and a total of 5 digits
        if not re.match(r'^\d{1,5}(\.\d{1,2})?$', duration):
            return "Invalid duration value."



        # Update the test record
        conn = sqlite3.connect('sea-assignment/database.db')
        cur = conn.cursor()
        cur.execute('''
            UPDATE Tests
            SET test_name=?, duration=?, region=?, audio_test_type=?, playback_type=?, test_criteria=?, test_parameters=?
            WHERE test_id=?
        ''', (test_name, duration, region, audio_test_type, playback_type, test_criteria, test_parameters, test_id))
        conn.commit()
        conn.close()

        return redirect('/tests')  # Redirect to the page displaying test records
    
@app.route('/admin/tests/delete', methods=['GET'])
def delete_test():
    test_id = request.args.get('test_id')
    conn = sqlite3.connect('sea-assignment/database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Tests WHERE test_id = ?", (test_id,))
    conn.commit()
    conn.close()
    return redirect('/tests')

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)