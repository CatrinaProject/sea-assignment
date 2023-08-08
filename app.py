import sqlite3
from flask import Flask, redirect, render_template, request, session, flash


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

@app.route('/admin/dashboard', methods=["GET", "POST"])
def admin_dashboard():
    if not is_admin():
        flash('You are not authorized to access the admin dashboard.', 'error')
        return redirect('/home')
    
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

            flash('Selected user(s) approved as admin successfully.', 'success')
        else:
            flash('No users selected for approval.', 'warning')

    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_type = 'regular' AND approved = 0")
    pending_users = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE user_type = 'admin' AND approved = 1")
    admins = cur.fetchall()

    con.close()

    return render_template('admin-dashboard.html', pending_users=pending_users, admins=admins)


@app.route('/admin/televisions/edit', methods=['GET'])
def edit_televisions():
    pass

@app.route('/admin/tests/edit', methods=['GET'])
def edit_tests():
    pass

@app.route('/logout')
def logout():
    session['username'] = None
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)