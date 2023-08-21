import sqlite3
from flask import redirect, render_template, request
from helpers import validate_bad_chars


def extract_television_form_values(tv_request):
    return {
        'brand': tv_request.form['brand'],
        'audio': tv_request.form['audio'],
        'resolution': tv_request.form['resolution'],
        'refresh_rate': tv_request.form['refresh_rate'],
        'screen_size': tv_request.form['screen_size']
    }


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
        form_values = extract_television_form_values(request)

        validate_bad_chars(params=form_values['brand'] + form_values['audio'] +
                                  form_values['resolution'] + form_values['refresh_rate'] +
                                  form_values['screen_size'])

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


def delete_television():
    tv_id = request.args.get('tv_id')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Televisions WHERE tv_id = ?", (tv_id,))
    conn.commit()
    conn.close()
    return redirect('/televisions')


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
