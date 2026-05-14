import customtkinter as ctk
import CTkListbox
from database import create_table, add_issue, get_issues

create_table()

def submit():
    issue_type = type_entry.get()
    description = desc_entry.get()
    location = loc_entry.get()

    add_issue(issue_type, description, location, "open")
    display_issues()

def display_issues():
    issue_list.delete("1.0", "end")

    issues = get_issues()

    for issue in issues:
        issue_list.insert("end", f"{issue}\n")

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

create_table()

root = ctk.CTk()
root.title("Issue Tracker")
root.geometry("400x700")

header = ctk.CTkLabel(
    root,
    text="Issue Tracker",
    font=ctk.CTkFont(size=24, weight="bold")
)

issues_label = ctk.CTkLabel(
    root,
    text="Active Issues",
    font=("Arial", 18)
)
issues_label.pack()



issue_frame = ctk.CTkFrame(
    root,
    width=300,
    height=400,
    corner_radius=30
    )
issue_frame.pack(pady=20)

issue_frame.pack_propagate(False)

issue_list = ctk.CTkTextbox(
    issue_frame,
    width=260,
    height=350
)

new_issue_button = ctk.CTkButton(
    root,
    text="NEW ISSUE",
    width=250,
    height=50,
    corner_radius=20
)
new_issue_button.pack(pady=20)


display_issues()
root.mainloop()