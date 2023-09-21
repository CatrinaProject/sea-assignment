import sqlite3
from flask import request, render_template


# Function used to render the admin dashboard
def admin_dashboard():
    if request.method == 'POST':  # If there is a POST request made to the admin_dashboard
        selected_users = request.form.getlist('approve_user')  # List of selected users from the checked checkboxes
        if selected_users:  # If selected_users is not empty, run database query to update the selected regular users
            con = sqlite3.connect('database.db')
            cur = con.cursor()

            for username in selected_users:  # with each username in the list of selected users, update them to admin
                # Update user_type to 'admin' and approved to 1 for the selected user(s)
                cur.execute('UPDATE users SET user_type = ?, approved = ? WHERE username = ?',
                            ('admin', 1, username))

            con.commit()
            con.close()
        else:
            return 'No users selected for approval.', 400

    con = sqlite3.connect('database.db')  # Connect to the database and get a list of admin and regular users
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE user_type = 'regular' AND approved = 0")  # Get all regular users
    pending_users = cur.fetchall()

    cur.execute("SELECT * FROM users WHERE user_type = 'admin' AND approved = 1")  # Get all admin users
    admins = cur.fetchall()

    con.close()

    # render the admin_dashboard with the regular (pending_users) and admin users
    return render_template('admin-dashboard.html', pending_users=pending_users, admins=admins)
