import sqlite3
conn = sqlite3.connect('issues.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS issues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
               issue_type TEXT,
               description TEXT,
               location TEXT,
               status TEXT
)''')

cursor.execute('''INSERT INTO issues (issue_type, description, location, status) VALUES (?, ?, ?, ?)
               ''', ('IT', 'Computer not working', 'Office', 'Open'))
conn.commit()
conn.close()