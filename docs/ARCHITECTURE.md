# System Architecture

## Simple Explanation
A student uploads a homework file from anywhere with internet access. The
teacher opens a dashboard, sees every submission in one place, grades it, and
the student instantly sees their marks and feedback — no email attachments,
no USB drives, no lost paperwork.

## Technical Explanation
The frontend never talks to a database or a file system directly. It calls a
REST API. The API authenticates the caller (JWT), authorizes the action
(role + ownership check), then either:
- reads/writes **metadata** (users, assignments, marks, feedback) in the
  **cloud database**, or
- reads/writes **file bytes** (the actual PDF/DOCX/ZIP) in **cloud object
  storage**, keeping only a reference (`storage_path`) in the database.

## Core Workflow
```
Teacher
  |
  v
Creates Assignment  --------------------->  Cloud Database (metadata)
  |
  v
Student Dashboard  <----------------------  Cloud Database (reads)
  |
  v
Student Uploads Assignment
  |
  v
Cloud Object Storage (file bytes)  ------>  storage_path returned
  |
  v
Submission Metadata Saved  --------------->  Cloud Database
  |
  v
Teacher Reviews Submission (downloads file, enters marks/feedback)
  |
  v
Cloud Database (marks + feedback saved)
  |
  v
Student Views Feedback
```

## Request / Data Flow (as built — Option A/B)
```
Browser (frontend/*.html + js/api.js)
        |  HTTPS + JSON / multipart
        v
Flask REST API (backend/app.py)
        |
        +--> Flask-JWT-Extended  -> validates identity + role
        |
        +--> SQLAlchemy (database.py) -> Cloud Database (SQLite -> Postgres/Firestore)
        |
        +--> storage_service.py -> Cloud Object Storage (local disk -> S3/Firebase)
```

## Advanced Cloud Architecture (Option C target)
```
Users
  |
  v
CDN (static frontend assets)
  |
  v
Frontend Hosting (S3+CloudFront / Netlify / Vercel)
  |
  v
API Gateway  (routing, throttling, auth pass-through)
  |
  v
Backend / Serverless Functions (Lambda / Cloud Run / App Runner)
  |
  v
Managed Database (RDS/DynamoDB/Firestore) + Object Storage (S3/Firebase Storage)
  |
  v
Monitoring / Logging (CloudWatch / Cloud Logging)
```
