Written By ChatGPT to help me streamline how im going to build my project


🧩 1. Recommended Tech Stack (Desktop)
✅ Best choice:
    Python + Tkinter (built-in, simple)
Better UI option (if you want higher marks):
    PyQt5 / PySide6 → more modern interface
Backend:
    SQLite (simple, no setup required)


🏗️ 2. Architecture (Simplified)
Desktop App (Tkinter / PyQt)
        ↓
Application Logic (Python)
        ↓
SQLite Database
        ↓
(Optional: File storage for images)


📋 3. Core Features
🔹 Must-have (MVP)
    Submit issue report
    Select:
        Issue type (Maintenance / IT)
        Description
        Location
    Save report to database
    View all reports
🔹 Extra (for higher grades)
Attach image
    Filter reports (IT vs Maintenance)
    Status system (Pending / Fixed)
    Search bar
    Admin mode


🛠️ 4. Step-by-Step Implementation Plan
Phase 1 — Setup

Install dependencies (if using PyQt):

    pip install PyQt5
    pip install pillow

(Tkinter doesn’t need installing)


Phase 2 — Database Setup (SQLite)

Create database:

    import sqlite3

    conn = sqlite3.connect("issues.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        description TEXT,
        location TEXT,
        status TEXT,
        image_path TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

Phase 3 — Build UI
Option A: Tkinter (simpler)

Create:

    Main window
    Form:
        Dropdown (Issue Type)
        Textbox (Description)
        Entry (Location)
        Button (Submit)

Phase 4 — Submit Report Logic
    def submit_report(issue_type, description, location):
        conn = sqlite3.connect("issues.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO reports (type, description, location, status)
        VALUES (?, ?, ?, ?)
        """, (issue_type, description, location, "Pending"))

        conn.commit()
        conn.close()

Phase 5 — Display Reports
Use a table view:
    Tkinter → Treeview
    PyQt → QTableWidget

Show:

    ID
    Type
    Description
    Location
    Status

Phase 6 — Add Image Upload (Optional)

Use file picker:

    from tkinter import filedialog

    file_path = filedialog.askopenfilename()

Store:

    Just the file path in database
    
Phase 7 — Status Update Feature

Add button:

    “Mark as Fixed”
        UPDATE reports SET status = "Fixed" WHERE id = ?

Phase 8 — Polish UI
    Add tabs:
        “Submit Issue”
        “View Issues”
    Add filters (dropdown)

📦 5. Dependencies Summary
Required:
    sqlite3 (built-in)
    tkinter (built-in)
Optional:
    PyQt5 / PySide6
    pillow (for images)

📁 6. Suggested Project Structure
    project/
    │
    ├── main.py
    ├── database.py
    ├── ui/
    │   ├── main_window.py
    │   ├── report_form.py
    │   ├── report_list.py
    │
    ├── assets/
    │   ├── images/
    │
    └── issues.db

⚠️ 7. Common Mistakes
    ❌ Not separating database logic from UI
    ❌ Hardcoding everything into one file
    ❌ Forgetting to commit database changes
    ❌ No input validation

🚀 8. Timeline
Day 1:
    Database + basic UI
Day 2:
    Submit + display reports
Day 3:
    Image + status system
Day 4:
    UI polish + testing

💡 Strong Recommendation
If your goal is:
    ✅ Fast completion → Tkinter
    ✅ Better marks / nicer UI → PyQt5