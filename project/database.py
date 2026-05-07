import sqlite3
def connect():
    return sqlite3.connect('issues.db')

def create_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS issues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_type TEXT,
                description TEXT,
                location TEXT,
                status TEXT
    )
                ''')
    conn.commit()
    conn.close()

def add_issue(issue_type, description, location, status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('''INSERT INTO issues (issue_type, description, location, status)
                      VALUES (?, ?, ?, ?)''', (issue_type, description, location, status))
    
    conn.commit()
    conn.close()
    
def get_issues():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM issues')
    rows = cursor.fetchall()

    conn.close()
    return rows

def update_issue_status(issue_id, new_status):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute('UPDATE issues SET status = ? WHERE id = ?', (new_status, issue_id))

    conn.commit()
    conn.close()


