# Cloud-Based Student Assignment Submission & Feedback Portal

A cloud-computing course project: a REST API + web frontend that lets
teachers create assignments with deadlines, students submit files that are
validated and time-stamped server-side, and teachers grade submissions and
return feedback — all gated by JWT authentication and role-based
authorization, with cloud database and cloud object storage kept as
cleanly separated, swappable concerns.

## Overview
See `reports/PROJECT_REPORT.md` for the full write-up (abstract, problem
statement, objectives, results, limitations, future scope).

## Problem Statement
Manual assignment collection (email attachments, shared drives, paper) has
no automated deadline enforcement, no centralized grading, and no audit
trail. This project centralizes that workflow.

## Objectives
- Demonstrate real cloud-computing concepts (see `docs/CLOUD_CONCEPTS.md`).
- Enforce role-based access control between students and teachers.
- Separate metadata (database) from file bytes (object storage).
- Ship a fully working, tested, documented, GitHub-ready reference build.

## Features
- Student & teacher registration/login (JWT-based)
- Role-based dashboards with live stats
- Assignment CRUD (teacher) with configurable allowed file types & max size
- Student upload / resubmission with server-side deadline enforcement
- `SUBMITTED` / `LATE` / `GRADED` status tracking
- Teacher grading with marks + written feedback
- File download restricted to the submission's owner or the teacher
- 22 automated pytest tests, all passing

## User Roles
See `docs/ROLES.md` for the full permission table (Student / Teacher / Admin-future).

## Cloud Computing Concepts
See `docs/CLOUD_CONCEPTS.md` — a concept-by-concept map to exactly where
it appears in this codebase (cloud DB, object storage, RBAC, REST API,
serverless path, scalability, CDN, secrets management, CI/CD, and more).

## Architecture
See `docs/ARCHITECTURE.md` for the full request/data-flow diagrams
(as-built and the advanced cloud-native target).

## Technology Stack
This repo implements **Option A (Beginner / free / local)**:
- Frontend: HTML, CSS, vanilla JavaScript
- Backend: Python Flask
- Database: SQLite (via SQLAlchemy)
- Storage: Local uploads folder (behind a swappable interface)

See `docs/TECH_STACK_OPTIONS.md` for Options B (managed cloud services,
recommended next step) and C (full AWS/Azure/GCP architecture).

## Database Design
See `docs/DATABASE_DESIGN.md` for the full schema, relationships, and
indexing rationale.

## Cloud Storage
See `cloud/storage_service.py` (design notes) and
`backend/storage_service.py` (working `LocalStorageService`
implementation) for the object-storage abstraction and how to swap in
S3/Firebase.

## Authentication & Authorization
JWT-based login issuing role claims; every protected route enforces
role-based access plus per-object ownership checks. See
`docs/SECURITY.md`.

## Assignment Workflow
Teacher creates assignment → stored in cloud database → visible on every
student's dashboard. See `docs/ARCHITECTURE.md`.

## Submission Workflow
Student selects assignment → file validated → uploaded to storage →
metadata saved → confirmation shown. Deadline is checked against the
**server clock**, never the client's. See `backend/routes/submission_routes.py`.

## Feedback & Grading
Teacher opens a submission, downloads/views the file, enters marks (capped
at the assignment's `max_marks`) and feedback; the student can view but
never edit either.

## REST APIs
Full endpoint reference in `docs/API_DOCUMENTATION.md`.

## Folder Structure
```
Cloud-Assignment-Submission-Portal/
├── frontend/            # HTML/CSS/JS client (login, dashboards, assignments, submissions)
├── backend/             # Flask REST API, models, routes, storage/auth logic
│   ├── app.py           # application factory + entrypoint
│   ├── config.py        # environment-driven configuration
│   ├── models.py        # SQLAlchemy models (User, Course, Assignment, Submission)
│   ├── database.py      # SQLAlchemy instance
│   ├── auth_utils.py    # RBAC decorator
│   ├── storage_service.py  # cloud object storage abstraction (local implementation)
│   ├── seed.py           # dummy teacher/student/course/assignment data
│   └── routes/           # auth, courses, assignments, submissions, dashboards
├── cloud/                # design-notes for the DB/storage/auth cloud abstractions
├── tests/                # pytest suite (22 tests)
├── sample_files/         # dummy sample submission files for demoing upload
├── screenshots/          # put your own proof screenshots here (see reports/)
├── docs/                 # architecture, API docs, security, scalability, etc.
├── reports/              # project report, resume/LinkedIn text, interview prep, GitHub strategy
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation & Local Setup
### 1. Clone and enter the project
```bash
cd Cloud-Assignment-Submission-Portal
```

### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Install backend dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# edit .env and set real SECRET_KEY / JWT_SECRET_KEY values
```

### 5. Seed dummy data (optional but recommended for first run)
```bash
cd backend
python seed.py
```
Expected output:
```
Seed data created:
  Teacher login -> teacher@example.com / Teacher@123
  Student login -> student1@example.com / Student@123
  Student login -> student2@example.com / Student@123
  Course: Cloud Computing 101 (id=1)
  Assignment: Assignment 1: Cloud Storage Basics (id=1)
```

### 6. Start the backend
```bash
python app.py
```
Expected output includes `Running on http://0.0.0.0:5000`.

### 7. Open the frontend
Open `frontend/login.html` directly in a browser (or serve the folder with
any static server, e.g. `python -m http.server 8080` from inside
`frontend/`). Log in with one of the seeded accounts above.

### 8–18. Demo the full workflow
1. Log in as the teacher, view the teacher dashboard.
2. Go to **Assignments**, create a new assignment for course id `1`.
3. Log out, log in as `student1@example.com`.
4. Go to **Assignments**, upload a file for the assignment (a file from
   `sample_files/` works great for this).
5. Confirm the status badge shows `SUBMITTED` (or `LATE` if past the
   deadline you set).
6. Check `backend/storage/assignments/` on disk — your uploaded file is there.
7. Log back in as the teacher, open **View Submissions** for that
   assignment — the metadata row is visible.
8. Click **Grade**, enter marks + feedback, save.
9. Log back in as the student — the assignment now shows the marks and
   **View Feedback** displays the teacher's comments.

## Environment Variables
See `.env.example` for the full list (secrets, database URL, storage
backend/root, upload limits, CORS, feature flags for late submission and
resubmission).

## Running the Application
See steps 6–7 above. `GET /api/health` is available for a quick liveness
check.

## Testing
```bash
cd tests
pytest -q
```
22 tests, all passing — see `docs/TESTING.md` for the full traceability
table back to the spec's 25-case testing strategy.

## Cloud Deployment
See `docs/DEPLOYMENT.md` for both a free-tier deployment path and a full
AWS/Azure/GCP architecture mapping.

## Security
See `docs/SECURITY.md`.
Teacher registration requires an invite code; admin accounts cannot be self-registered.

## Scalability
See `docs/SCALABILITY.md`.

## Failure Handling
- **Upload fails mid-transfer:** the client sees a clear error; no partial
  metadata row is ever created without a successfully saved file.
- **Deadline passed but late submissions disabled:** the uploaded file is
  deleted from storage (rolled back) and a `403` is returned — no orphaned
  file is left behind.
- **Duplicate submission with resubmission disabled:** rejected with `409`
  before any file write is attempted.
- **Database/storage unavailable:** caught by Flask's global error
  handlers and returned as a generic `500` — no internal details leak to
  the client.
- **Expired auth token:** any protected route returns `401`; the frontend
  redirects to the login page.

## Screenshots
Capture your own run-through using the checklist in
`reports/GITHUB_PROOF_STRATEGY.md` and save them under `screenshots/`.

## Results
22/22 automated tests passing; full manual workflow (create → upload →
grade → view feedback) verified end-to-end. See `reports/PROJECT_REPORT.md`.

## Limitations
Single-teacher-per-assignment ownership, no malware scanning yet, admin
role scoped but not implemented, local storage is a stand-in for a real
object store (by design, for a $0 local setup).

## Future Improvements
Admin role & user management, email notifications, real-time submission
status via WebSockets, plagiarism-detection integration, a full React
frontend (Option B).

## Learning Outcomes
Cloud database vs. object storage separation, REST API design,
authentication vs. authorization, role-based access control, server-side
deadline enforcement, automated testing, and cloud deployment planning
across three cost/complexity tiers.

## Author
Student project — Cloud Computing coursework.

---
See also: `reports/RESUME_AND_LINKEDIN.md`, `reports/INTERVIEW_PREP.md`,
and `reports/GITHUB_PROOF_STRATEGY.md` for turning this into a polished
GitHub/resume/interview asset.
