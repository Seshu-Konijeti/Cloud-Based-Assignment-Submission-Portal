"""
config.py
Centralized configuration loaded from environment variables.
Never hardcode secrets here — this file only reads them.
"""

from dotenv import load_dotenv
load_dotenv()
import os
from datetime import timedelta

class Config:
    # --- Core Flask config ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-.env")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-me-in-.env")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.environ.get("JWT_EXPIRES_HOURS", 8)))

    # --- Database (Cloud DB in production: Firestore/Supabase Postgres/RDS/DynamoDB) ---
    # For local/free-tier development we use SQLite, which mimics a managed
    # cloud database's role: it stores users, courses, assignments, submission
    # METADATA, marks and feedback — never the actual files.
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'portal.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Object storage (Cloud Storage in production: S3/Firebase/Supabase Storage) ---
    # STORAGE_BACKEND can be "local" (default, free) or "s3" (future extension).
    STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "local")
    LOCAL_STORAGE_ROOT = os.environ.get(
        "LOCAL_STORAGE_ROOT", os.path.join(BASE_DIR, "storage", "assignments")
    )

    # --- Upload validation ---
    ALLOWED_EXTENSIONS = set(
        os.environ.get("ALLOWED_EXTENSIONS", "pdf,doc,docx,zip,png,jpg,jpeg").split(",")
    )
    MAX_FILE_SIZE_MB = int(os.environ.get("MAX_FILE_SIZE_MB", 10))
    MAX_CONTENT_LENGTH = MAX_FILE_SIZE_MB * 1024 * 1024

    # --- CORS ---
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # --- Feature flags ---
    TEACHER_INVITE_CODE = os.environ.get("TEACHER_INVITE_CODE", "")
    ALLOW_LATE_SUBMISSION = os.environ.get("ALLOW_LATE_SUBMISSION", "true").lower() == "true"
    ALLOW_RESUBMISSION = os.environ.get("ALLOW_RESUBMISSION", "true").lower() == "true"
