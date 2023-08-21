import sqlite3
import re
from flask import redirect, render_template, request
from helpers import validate_bad_chars, is_admin


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


def tests():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    # Get all the test records to be viewed on the page as a list
    cur.execute("SELECT * FROM tests")
    test_cases = cur.fetchall()
    con.commit()
    con.close()
    return render_template('tests.html', test_cases=test_cases)


def add_test_record():
    if request.method == 'POST':
        form_values = extract_tests_form_values(request)

        validate_bad_chars(
            params=form_values['test_name'] + form_values['duration'] + form_values['region']
                   + form_values['audio_test_type'] + form_values['playback_type'] + form_values['test_criteria']
                   + form_values['test_parameters'])

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


def delete_test():
    test_id = request.args.get('test_id')
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Tests WHERE test_id = ?", (test_id,))
    conn.commit()
    conn.close()
    return redirect('/tests')
