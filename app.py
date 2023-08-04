import sqlite3
from flask import Flask, redirect, render_template, request, session


def register_user_to_db(username, password):
    con = sqlite3.connect('sea-assignment/database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO users(username,password) VALUES (?,?)', (username, password))
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
        return redirect("/")


@app.route('/home', methods=['POST', "GET"])
def home():
    if 'username' in session:
        # TODO Update the home.html with more functionality
        return render_template('home.html', username=session['username'])
    else:
        # TODO Add a failed login page
        return "Username or Password is wrong!"


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)