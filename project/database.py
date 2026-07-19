"""Simple SQLite helper for the Issue Tracker application.

This module provides a connection helper and basic CRUD operations.
"""

import sqlite3  # sqlite library for DB access


def connect():
    """Return a new connection to the issues database.

    Returns:
        sqlite3.Connection: a connection object to 'issues.db'.
    """
    return sqlite3.connect('issues.db')  # open (or create) the DB file

def create_table():
    'Called create_table() before the GUI loads to ensure the database and table are created before any data is accessed.'
    conn = connect()  # get a DB connection
    cursor = conn.cursor()  # create a cursor for SQL commands

    cursor.execute('''CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_type TEXT,
                description TEXT,
                location TEXT,
                status TEXT
    )
                ''')  # create the issues table if missing
    conn.commit()  # save changes
    conn.close()  # close DB connection

def add_issue(issue_type, description, location, status):
    """Insert a new issue into the database.

    Prevents inserting the exact same issue twice in a row by checking the
    most recently inserted row. Returns True when an insert occurred and
    False when the insert was skipped because it appeared to be a duplicate.

    Raises sqlite3.Error for unexpected database errors.
    """
    conn = None  # placeholder for connection
    try:
        conn = connect()  # open DB connection
        cursor = conn.cursor()  # get cursor for SQL

        # Check the most recent row to avoid accidental duplicate submissions
        cursor.execute(
            'SELECT issue_type, description, location, status FROM issues '
            'ORDER BY id DESC LIMIT 1'
        )  # query last row
        last = cursor.fetchone()  # fetch one row

        if last and last == (issue_type, description, location, status):
            # Duplicate of the immediately previous record — skip insert
            conn.close()  # close connection
            return False  # indicate no insert was done

        cursor.execute(
            'INSERT INTO issues (issue_type, description, location, status) '
            'VALUES (?, ?, ?, ?)',
            (issue_type, description, location, status)
        )  # insert new issue

        conn.commit()  # commit the insert
        conn.close()  # close connection
        return True  # indicate insert succeeded
    except sqlite3.Error:
        # Ensure the connection is closed on error and re-raise
        if conn:
            conn.close()  # close if open
        raise  # propagate error
    
def get_issues():
    conn = connect()  # open DB connection
    cursor = conn.cursor()  # create cursor

    cursor.execute('SELECT * FROM issues')  # select all rows
    rows = cursor.fetchall()  # fetch all results

    conn.close()  # close connection
    return rows  # return rows to caller

def update_issue_status(issue_id, new_status):
    conn = connect()  # open DB connection
    cursor = conn.cursor()  # create cursor

    cursor.execute('UPDATE issues SET status = ? WHERE id = ?', (new_status, issue_id))  # update row

    conn.commit()  # save changes
    conn.close()  # close connection


