import sqlite3
from flask import request, render_template


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
