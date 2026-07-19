"""Issue Tracker application.

This program provides a small GUI for creating and managing IT issue
reports. It uses CustomTkinter for the interface and an SQLite
database for persistence.
"""

from typing import List, Optional, Tuple

from typing import List, Optional, Tuple  # typing helpers

import customtkinter as ctk  # customtkinter UI toolkit
import tkinter.messagebox as messagebox  # simple message dialogs
import sqlite3  # sqlite database module
from database import (  # database helper functions
    create_table,  # create DB table
    add_issue,  # insert new issue
    get_issues,  # fetch issues
    update_issue_status,  # update issue status
)

from CTkListbox import CTkListbox  # custom listbox widget

create_table()  # ensure DB table exists before UI starts

current_issues_data: List[Tuple] = []  # cached issues from DB
selected_issue_id: Optional[int] = None  # id of selected issue


def submit():
    """Submit a new issue to the database.

    Performs input validation, attempts to insert into the database and
    provides user feedback on success or failure.
    """
    issue_type = type_entry.get().strip()  # read and trim type field
    description = desc_entry.get().strip()  # read and trim description
    location = loc_entry.get().strip()  # read and trim location
    # Input validation: required fields and maximum lengths
    errors = []  # collect validation errors

    if not issue_type:
        errors.append("Issue Type cannot be blank.")  # require type
    if not description:
        errors.append("Description cannot be blank.")  # require description
    if not location:
        errors.append("Location cannot be blank.")  # require location

    if len(issue_type) > 100:
        errors.append("Issue Type must be 100 characters or fewer.")  # limit type
    if len(location) > 100:
        errors.append("Location must be 100 characters or fewer.")  # limit location
    if len(description) > 500:
        errors.append("Description must be 500 characters or fewer.")  # limit desc

    if errors:
        messagebox.showerror("Validation Error", "\n".join(errors))  # show errors
        return  # stop on validation failure

    # All validations passed — attempt to add the issue and handle DB errors
    try:
        inserted = add_issue(issue_type, description, location, "open")  # try insert
    except sqlite3.Error as exc:  # pragma: no cover - DB runtime error
        messagebox.showerror("Database Error", f"An error occurred: {exc}")  # show DB error
        return  # stop on DB error

    if not inserted:
        # add_issue returns False when it detects an immediate duplicate
        messagebox.showinfo(
            "Duplicate Issue",
            "This issue appears to be a duplicate and was not added.",
        )  # inform user about duplicate
        return  # do not clear form

    # Success
    messagebox.showinfo("Success", "Issue submitted successfully.")  # success dialog
    try:
        display_issues()  # refresh list
    except sqlite3.Error:
        # display_issues already reports the error to the user
        pass  # ignore repeated error

    type_entry.delete(0, "end")  # clear type entry
    desc_entry.delete(0, "end")  # clear description entry
    loc_entry.delete(0, "end")  # clear location entry

    show_home()  # return to home view


def display_issues():
    """Load all issues from the database and display them.

    Preserves and highlights the currently selected issue if present.
    """
    global current_issues_data

    issue_list.delete("all")  # clear existing listbox items

    try:
        current_issues_data = get_issues()  # fetch rows from DB
    except sqlite3.Error as exc:
        messagebox.showerror("Database Error", f"Failed to load issues: {exc}")  # show DB error
        current_issues_data = []  # fallback to empty list

    for issue in current_issues_data:
        _, issue_type, description, location, status = issue  # unpack row

        icon = "[Open]" if status == "open" else "[Closed]"  # choose icon
        display_text = f"{icon} | {issue_type} | {location}"  # build display text

        issue_list.insert("end", display_text)  # add item to listbox

    # Highlight the previously selected issue, if it still exists
    if selected_issue_id is not None and current_issues_data:
        for idx, issue in enumerate(current_issues_data):
            if issue[0] == selected_issue_id:
                try:
                    issue_list.selection_set(idx)  # select the same index
                except Exception:
                    # Some listbox implementations may not support selection_set
                    pass
                break


def on_issue_click(selected_value):
    """Display the selected issue's details and enable the Save button.

    The callback receives the value provided by the listbox widget but
    uses `curselection()` to find the integer index. The function
    safely handles unexpected selections.
    """
    global selected_issue_id

    try:
        sel = issue_list.curselection()

        # Support different return types from listbox implementations:
        # - tuple/list of indices (e.g., (0,))
        # - a single int (e.g., 0)
        if sel is None or not current_issues_data:
            selected_issue_id = None  # no valid selection
            save_button.configure(state="disabled")  # disable Save
            return

        if isinstance(sel, (tuple, list)):
            if len(sel) == 0:
                selected_issue_id = None  # empty tuple/list
                save_button.configure(state="disabled")  # disable Save
                return
            idx = int(sel[0])  # first index from tuple/list
        else:
            # Could be an int or a string index
            idx = int(sel)  # single value selection
        clicked_issue = current_issues_data[idx]  # get the clicked row

        issue_id, issue_type, description, location, status = clicked_issue
        selected_issue_id = issue_id

        type_label.configure(text=f"Type: {issue_type}")
        location_label.configure(text=f"Location: {location}")
        status_label.configure(text=f"Status: {status}")
        status_dropdown.set(status)
        description_label.configure(text=f"Description:\n\n{description}")

        # Ensure the Save button is enabled now that an issue is selected
        save_button.configure(state="normal")  # enable Save button

        # Highlight selection in the listbox for better visibility
        try:
            issue_list.selection_clear(0, "end")  # clear previous selection
            issue_list.selection_set(idx)  # set new selection
        except Exception:
            pass  # ignore if unsupported

        show_issue_details()  # switch to details view
    except Exception as exc:  # pragma: no cover - UI edge cases
        messagebox.showerror("Error", f"Failed to select issue: {exc}")  # show error


def show_new_issue():
    """Display the new issue screen."""
    home_frame.pack_forget()
    new_issue_frame.pack(fill="both", expand=True)


def show_home():
    """Display the home screen."""
    new_issue_frame.pack_forget()
    issue_details_frame.pack_forget()
    home_frame.pack(fill="both", expand=True)
    # When returning home, clear any selection and disable Save
    try:
        issue_list.selection_clear(0, "end")
    except Exception:
        pass
    save_button.configure(state="disabled")


def show_issue_details():
    """Display the issue details screen."""
    home_frame.pack_forget()
    issue_details_frame.pack(fill="both", expand=True)


def save_status():
    """Save the updated status of the selected issue."""
    if selected_issue_id is None:
        messagebox.showwarning("No Selection", "No issue selected to update.")
        save_button.configure(state="disabled")
        return

    new_status = status_dropdown.get()
    confirm = messagebox.askyesno(
        "Confirm Status Change",
        f"Change the status of the selected issue to '{new_status}'?",
    )
    if not confirm:
        return

    try:
        update_issue_status(selected_issue_id, new_status)
    except sqlite3.Error as exc:
        messagebox.showerror("Database Error", f"Failed to update status: {exc}")
        return

    try:
        display_issues()
    except sqlite3.Error:
        pass

    messagebox.showinfo("Success", "Issue status updated.")
    show_home()


ctk.set_appearance_mode("dark")

ctk.set_default_color_theme("blue")

create_table()

root = ctk.CTk()
root.title("Issue Tracker")
root.geometry("400x630")


def _report_callback_exception(exc, val, tb):
    """Global handler for uncaught Tkinter exceptions.

    This prevents the application from crashing silently and shows a
    user-friendly error dialog so the assessor can capture the error.
    """
    messagebox.showerror("Unexpected Error", f"{exc}: {val}")


# Attach the global exception handler so unhandled callback errors are shown
root.report_callback_exception = _report_callback_exception

home_frame = ctk.CTkFrame(root)
home_frame.pack(fill="both", expand=True)

new_issue_frame = ctk.CTkFrame(root)
issue_details_frame = ctk.CTkFrame(root)

details_title = ctk.CTkLabel(
    issue_details_frame,
    text="Issue Details",
    font=ctk.CTkFont(size=24, weight="bold")
)
details_title.pack(pady=20)

type_label = ctk.CTkLabel(
    issue_details_frame,
    text="Type: "
)
type_label.pack(pady=5)

location_label = ctk.CTkLabel(
    issue_details_frame,
    text="Location: "
)
location_label.pack(pady=5)

status_label = ctk.CTkLabel(
    issue_details_frame,
    text="Status: "
)
status_label.pack(pady=5)

status_dropdown = ctk.CTkOptionMenu(
    issue_details_frame,
    values=["open", "closed"]
)
status_dropdown.pack(pady=10)

save_button = ctk.CTkButton(
    issue_details_frame,
    text="Save",
    command=save_status
)
save_button.pack(pady=10)
save_button.configure(state="disabled")

description_label = ctk.CTkLabel(
    issue_details_frame,
    text="Description:",
    wraplength=320,
    justify="left"
)
description_label.pack(pady=10)

back_details_button = ctk.CTkButton(
    issue_details_frame,
    text="Back",
    command=show_home
)
back_details_button.pack(pady=20)

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
    command=submit,
    font=("Bahnschrift", 14, "bold")
)
submit_button.pack(pady=20)

back_button = ctk.CTkButton(
    new_issue_frame,
    text="Back",
    width=100,
    height=30,
    corner_radius=15,
    fg_color="gray",
    command=show_home,
    font=("Bahnschrift", 14, "bold")
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
    font=("Bahnschrift", 18)
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

header_label = ctk.CTkLabel(
    issue_frame,
    text="Status | Type | Location",
    font=("Bahnschrift", 20, "bold")
)
header_label.pack(pady=(10, 0))

issue_list = CTkListbox(
    issue_frame,
    width=260,
    height=350,
    command=on_issue_click,
    font=("Bahnschrift", 14, "bold")
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
    font=("Bahnschrift", 14, "bold")
)
new_issue_button.pack(pady=20)

display_issues()
root.mainloop()
