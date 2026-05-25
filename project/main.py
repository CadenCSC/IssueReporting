import customtkinter as ctk
from database import create_table, add_issue, get_issues, update_issue_status

from CTkListbox import CTkListbox  

create_table()

current_issues_data = []

def submit():
    issue_type = type_entry.get().strip()
    description = desc_entry.get().strip()
    location = loc_entry.get().strip()

    if issue_type and description and location:
        add_issue(issue_type, description, location, "open")
        display_issues()

        type_entry.delete(0, "end")
        desc_entry.delete(0, "end")
        loc_entry.delete(0, "end")

        show_home()

def display_issues():
    global current_issues_data

    issue_list.delete("all")

    current_issues_data = get_issues()

    for issue in current_issues_data:
        issue_id, issue_type, description, location, status = issue

        icon = "🔴 [Open]" if status == "open" else "🟢 [Closed]"
        display_text = f"{icon} {issue_type} | {location} ({description})"

        issue_list.insert("end", display_text)

def on_issue_click(selected_value):
    selected_index = issue_list.curselection()

    if selected_index is not None and current_issues_data:
        clicked_issue = current_issues_data[selected_index]

        issue_id = clicked_issue[0]
        current_status = clicked_issue[4]

        new_status = "closed" if current_status == "open" else "open"

        update_issue_status(issue_id, new_status)
        display_issues()

def show_new_issue():
    home_frame.pack_forget()
    new_issue_frame.pack(fill="both", expand=True)

def show_home():
    new_issue_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

create_table()

root = ctk.CTk()
root.title("Issue Tracker")
root.geometry("400x630")

home_frame = ctk.CTkFrame(root)
home_frame.pack(fill="both", expand=True)

new_issue_frame = ctk.CTkFrame(root)

new_issue_title = ctk.CTkLabel(
    new_issue_frame,
    text="Create New Issue",
    font=ctk.CTkFont(size=24, weight="bold")
)
new_issue_title.pack(pady=20)

type_entry = ctk.CTkEntry(
    new_issue_frame,
    placeholder_text="Issue Type"
)
type_entry.pack(pady=10)

desc_entry = ctk.CTkEntry(
    new_issue_frame,
    placeholder_text="Description"
)
desc_entry.pack(pady=10)

loc_entry = ctk.CTkEntry(
    new_issue_frame,
    placeholder_text="Location"
)
loc_entry.pack(pady=10)

submit_button = ctk.CTkButton(
    new_issue_frame,
    text="Submit",
    width=200,
    height=40,
    corner_radius=20,
    fg_color="green",
    command=submit
)
submit_button.pack(pady=20)

back_button = ctk.CTkButton(
    new_issue_frame,
    text="Back",
    width=100,
    height=30,
    corner_radius=15,
    fg_color="gray",
    command=show_home
)
back_button.pack(pady=10)

header = ctk.CTkLabel(
    home_frame,
    text="Issue Tracker",
    font=ctk.CTkFont(size=24, weight="bold")
)

header.pack(pady=20)

issues_label = ctk.CTkLabel(
    home_frame,
    text="Active Issues",
    font=("Arial", 18)
)
issues_label.pack()



issue_frame = ctk.CTkFrame(
    home_frame,
    width=300,
    height=400,
    corner_radius=30
    )
issue_frame.pack(pady=20)

issue_frame.pack_propagate(False)

issue_list = CTkListbox(
    issue_frame,
    width=260,
    height=350,
    command=on_issue_click
)
issue_list.pack(pady=20)

new_issue_button = ctk.CTkButton(
    home_frame,
    text="NEW ISSUE",
    width=250,
    height=50,
    corner_radius=20,
    fg_color="red",
    command=show_new_issue,
    font=("Segoe UI Emoji", 14)
)
new_issue_button.pack(pady=20)


display_issues()
root.mainloop()