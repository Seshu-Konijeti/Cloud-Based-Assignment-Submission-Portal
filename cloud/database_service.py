"""
cloud/database_service.py

This file documents the CLOUD DATABASE abstraction used by the project.
The actual implementation lives in backend/database.py + backend/models.py
via Flask-SQLAlchemy, pointed at SQLite for local/free-tier development.

WHY THIS MATTERS FOR THE "CLOUD" STORY:
Because every route talks to `db.session` / model classes and never to
raw SQL file paths, swapping SQLITE_DATABASE_URI for a managed cloud
database connection string is a ONE-LINE config change:

    DATABASE_URL=postgresql://user:pass@your-project.supabase.co:5432/postgres
    # or
    DATABASE_URL=<Firestore/DynamoDB adapter connection string>

No route, model, or business-logic file needs to change.

WHAT IS STORED HERE (never files):
- users            (identity + role)
- courses          (teacher ownership)
- assignments      (title, description, deadline, max_marks, rules)
- submissions      (metadata: file_name, storage_path, status, marks, feedback)

WHAT IS NEVER STORED HERE:
- The actual PDF/DOCX/ZIP bytes -- those go to storage_service.py
  (cloud OBJECT STORAGE), referenced only by `storage_path`.
"""
