import sqlite3
from flask import redirect, render_template, request, session, flash
from helpers import validate_bad_chars, is_admin, validate_decimal


def extract_tests_form_values(test_request):  # Form a dictionary of values from the request
    return {
        'test_name': test_request.form['test_name'],
        'duration': test_request.form['duration'],
        'region': test_request.form['region'],
        'audio_test_type': test_request.form['audio_test_type'],
        'playback_type': test_request.form['playback_type'],
        'test_criteria': test_request.form['test_criteria'],
        'test_parameters': test_request.form['test_parameters'],
        'author_id': test_request.form['author_id']
    }


def validate_test_results(form_values):  # Pass the values in the dictionary into validation function
    validation_result = validate_bad_chars(
        form_values['test_name'] + form_values['duration'] + form_values['region']
        + form_values['audio_test_type'] + form_values['playback_type'] + form_values['test_criteria']
        + form_values['test_parameters'] + form_values['author_id'])
    validate_duration = validate_decimal(form_values['duration'])
    if validation_result is not None:
        return validation_result  # Return the error message directly
    elif validate_duration is not None:
        return validate_duration

def check_author_exists(author_id_from_request):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    
    # Return true/false whether the author_id exists. 
    cur.execute("SELECT EXISTS(SELECT 1 FROM users WHERE id = ?) AS id_exists", (author_id_from_request,))
    result = cur.fetchone()

    con.close()

    return result[0]

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
        form_values = extract_tests_form_values(request)  # Get a dictionary of values from the request

        if validate_test_results(form_values) is not None:
            return validate_test_results(form_values)
        
        if check_author_exists(form_values['author_id']):
            author_id = form_values['author_id']
        else:
            author_id = None

        # Insert new test record with parameters submitted by the user
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO Tests (
                        test_name, duration, region, audio_test_type, playback_type, test_criteria, test_parameters, author_id
                        )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) ''',
                    (form_values['test_name'], form_values['duration'], form_values['region'],
                     form_values['audio_test_type'], form_values['playback_type'], form_values['test_criteria'],
                     form_values['test_parameters'], author_id))

        session['last_added_test_id'] = cur.lastrowid

        conn.commit()
        conn.close()

        flash("Successfully added a new test record", "success")
        return redirect('/tests')  # Redirect to the page displaying television records


def edit_tests():
    test_id = request.args.get('test_id')  # Get the test_id from the request
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Tests WHERE test_id = ?", (test_id,))  # Get the test details for the test_id
    test_record = cur.fetchone()
    conn.close()

    # Check if the user is an admin OR if the last added test is the same in the session
    # Then render the edit-tests page
    if is_admin() or (session.get('last_added_test_id') and session['last_added_test_id'] == int(test_id)):
        return render_template('edit-tests.html', test_id=test_id, test_name=test_record[1], duration=test_record[2],
                               region=test_record[3], audio_test_type=test_record[4], playback_type=test_record[5],
                               test_criteria=test_record[6], test_parameters=test_record[7])
    else:
        flash("Sorry, you don't have permission to edit this record.", "error")
        return redirect("/tests")


def update_test_record():
    if request.method == 'POST':
        form_values = extract_tests_form_values(request)  # Get a dictionary of values from the request

        if validate_test_results(form_values) is not None:
            return validate_test_results(form_values)  # Validate those values in the dictionary

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
        flash("Successfully updated a test record", "success")
        return redirect('/tests')  # Redirect to the page displaying test records


def delete_test():
    test_id = request.args.get('test_id')  # Get the test_id from the request arguments
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM Tests WHERE test_id = ?", (test_id,))  # Delete the test_id record from the table
    conn.commit()
    conn.close()
    flash("Successfully deleted a test record", "success")
    return redirect('/tests')
