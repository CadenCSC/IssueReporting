import tkinter as tk
from database import create_table, add_issue, get_issues

create_table()

def submit():
    issue_type = type_entry.get()
    description = desc_entry.get()
    location = loc_entry.get()

    add_issue(issue_type, description, location, "open")
    print(get_issues())

root = tk.Tk()
root.title("Issue Tracker")

tk.Label(root, text="Issue Type").pack()
type_entry = tk.Entry(root)
type_entry.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Location").pack()
loc_entry = tk.Entry(root)
loc_entry.pack()

btn = tk.Button(root, text="Submit", command=submit).pack(pady=10)

root.mainloop()