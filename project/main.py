import tkinter as tk
from tkinter import Listbox
from database import create_table, add_issue, get_issues

create_table()

def submit():
    issue_type = type_entry.get()
    description = desc_entry.get()
    location = loc_entry.get()

    add_issue(issue_type, description, location, "open")
    display_issues()

def display_issues():
    issue_list.delete(0, tk.END)

    issues = get_issues()

    for issue in issues:
        issue_list.insert(tk.END, issue)

root = tk.Tk()
root.title("Issue Tracker")
root.geometry("500x900")

tk.Label(root, text="Issue Type").pack()
type_entry = tk.Entry(root)
type_entry.pack()

tk.Label(root, text="Description").pack()
desc_entry = tk.Entry(root)
desc_entry.pack()

tk.Label(root, text="Location").pack()
loc_entry = tk.Entry(root)
loc_entry.pack()

issue_list = Listbox(root, width=70)
issue_list.pack(pady=20)

btn = tk.Button(root, text="Submit", command=submit).pack(pady=10)

display_issues()
root.mainloop()