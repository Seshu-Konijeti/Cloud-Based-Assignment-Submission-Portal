"""
database.py
Initializes the SQLAlchemy extension shared across the app.
In OPTION B/C this same interface could point at Firestore/Supabase/RDS
instead of SQLite -- the rest of the app only talks to `db`, never to
the file system directly, which is what makes swapping the backing
cloud database possible without touching business logic.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
