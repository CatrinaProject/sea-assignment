import sqlite3
from flask import redirect, render_template, request, session, flash
from helpers import validate_bad_chars, is_admin


def extract_television_form_values(tv_request):  # Form a dictionary of values from the request
    return {
        'brand': tv_request.form['brand'],
        'audio': tv_request.form['audio'],
        'resolution': tv_request.form['resolution'],
        'refresh_rate': tv_request.form['refresh_rate'],
        'screen_size': tv_request.form['screen_size']
    }


def validate_television_results(form_values):  # Pass the values in the dictionary into validation function
    validation_result = validate_bad_chars(form_values['brand'] + form_values['audio'] +
                                           form_values['resolution'] + form_values['refresh_rate'] +
                                           form_values['screen_size'])

    if validation_result is not None:
        return redirect('/televisions')  # Redirect page and show error


def televisions():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM televisions")  # Get all the television records to be viewed on the page as a list
    television_results = cur.fetchall()
    con.commit()
    con.close()
    return render_template('televisions.html', television_results=television_results)


def add_television_record():
    if request.method == 'POST':
        form_values = extract_television_form_values(request)  # Get a dictionary of values from the request

        if validate_television_results(form_values) is not None:
            return validate_television_results(form_values)

        # Insert new television record with parameters submitted by the user
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Televisions (brand, audio, resolution, refresh_rate, screen_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (form_values['brand'], form_values['audio'], form_values['resolution'],
              form_values['refresh_rate'], form_values['screen_size']))

        session['last_added_tv_id'] = cur.lastrowid
        conn.commit()
        conn.close()

        flash('Successfully added a new television record', 'success')
        return redirect('/televisions')  # Redirect to the page displaying television records


def edit_television():
    tv_id = request.args.get('tv_id')
    # Get the requested television record with the user requested tv_id
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Televisions WHERE tv_id = ?", (tv_id,))
    tv_record = cur.fetchone()
    conn.close()

    # Check if the user is an admin OR if the last added television is the same in the session
    # Then render the edit-televisions page
    if is_admin() or (session.get('last_added_tv_id') and session['last_added_tv_id'] == int(tv_id)):
        return render_template('edit-televisions.html', tv_id=tv_id, brand=tv_record[1], audio=tv_record[2],
                               resolution=tv_record[3], refresh_rate=tv_record[4], screen_size=tv_record[5])
    else:
        flash("Sorry, you don't have permission to edit this record.", "success")
        return redirect("/home")


def delete_television():
    tv_id = request.args.get('tv_id')  # Get the tv_id
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Televisions WHERE tv_id = ?", (tv_id,))  # Delete the tv_id record from the table
    conn.commit()
    conn.close()
    flash("Successfully deleted television record", "success")
    return redirect('/televisions')


def update_television_record():
    if request.method == 'POST':
        form_values = extract_television_form_values(request)  # Get a dictionary of values from the request

        if validate_television_results(form_values) is not None:
            return validate_television_results(form_values)  # Validate those values in the dictionary

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
        flash("Successfully updated television record", "success")
        return redirect('/televisions')  # Redirect to the page displaying television records
