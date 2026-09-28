# Project Report: Cloud-Based Student Assignment Submission & Feedback Portal

## Abstract
This project implements a cloud-oriented web platform that lets teachers
publish assignments with deadlines and lets students submit files against
them from anywhere, with teachers grading and returning feedback through
the same system. It demonstrates the separation of cloud database
(metadata) from cloud object storage (files), REST API design,
authentication and role-based authorization, deadline enforcement, and a
testable, deployable architecture.

## Introduction
Manual assignment collection (email attachments, USB drives, paper) does
not scale, is easy to lose, and gives no visibility into who has/hasn't
submitted. This project centralizes that workflow behind a REST API backed
by a cloud database and cloud object storage.

## Problem Statement
Build a system where a teacher can create assignments with deadlines,
students can submit files that are validated and time-stamped
server-side, and teachers can grade and return feedback — without manual
file handling or spreadsheets.

## Objectives
- Demonstrate real cloud-computing concepts, not just a file-upload form.
- Enforce role-based access control between students and teachers.
- Separate metadata (database) from file bytes (object storage).
- Provide a fully working, tested, and documented reference implementation.

## Existing System
Typically: email attachments, shared drive folders, or paper submission —
no automated deadline enforcement, no centralized grading record, no
audit trail of who submitted what and when.

## Proposed System
A REST API (Flask) backed by a relational database for metadata and an
object-storage abstraction for files, consumed by a lightweight web
frontend, with JWT authentication and role-based authorization gating
every action.

## User Roles
See `docs/ROLES.md` for the full permission table (Student, Teacher, and a
scoped-out Admin role for future work).

## Cloud Computing Concepts
See `docs/CLOUD_CONCEPTS.md` for a concept-by-concept mapping to this
codebase.

## Technology Stack
See `docs/TECH_STACK_OPTIONS.md`. This repository implements Option A
(Flask + SQLite + local storage) with a documented, drop-in path to Option
B (managed cloud DB/storage/auth) and Option C (full AWS/Azure/GCP).

## System Architecture
See `docs/ARCHITECTURE.md`.

## Database Design
See `docs/DATABASE_DESIGN.md`.

## Cloud Storage Design
See `cloud/storage_service.py` and `backend/storage_service.py`.

## Authentication
JWT-based, implemented in `backend/auth_utils.py` and
`backend/routes/auth_routes.py`. See `docs/SECURITY.md`.

## Assignment Management
CRUD implemented in `backend/routes/assignment_routes.py`, restricted to
the teacher who owns the assignment (or an admin).

## Submission Workflow
Implemented in `backend/routes/submission_routes.py`: file-type/size
validation, server-side deadline comparison, resubmission handling
(overwrites the previous file and increments `attempt_number`), and
consistent `SUBMITTED` / `LATE` / `GRADED` status tracking.

## Deadline Management
Deadlines are stored and compared in UTC on the server; the client's clock
is never trusted for this decision (see the comment in
`submission_routes.py::submit_assignment`).

## Feedback & Grading
`POST /submissions/{id}/grade` validates that marks fall within
`0..max_marks`, restricted to teachers/admins; students can view but never
modify their own marks or feedback.

## API Design
See `docs/API_DOCUMENTATION.md` for every endpoint, its auth requirements,
and status codes.

## Implementation
Complete, runnable source under `backend/` and `frontend/` — see the root
`README.md` for setup instructions.

## Testing
24 automated pytest cases covering authentication, authorization,
assignment CRUD, and the full submission/grading workflow — see
`docs/TESTING.md`. All currently pass.

## Cloud Deployment
See `docs/DEPLOYMENT.md` for free-tier and AWS/Azure/GCP deployment paths.

## Security
See `docs/SECURITY.md`.

## Scalability
See `docs/SCALABILITY.md`.

## Results
A working end-to-end demo: a teacher account creates a course and
assignment, two student accounts submit (one on time, one late via a
resubmission), the teacher grades both, and each student sees their own
marks/feedback but not each other's, confirmed by the automated test
suite (24/24 passing).

## Advantages
Centralized submissions, automated deadline/late tracking, clear
separation of concerns that mirrors real cloud architecture, and a
codebase small enough for a single student to fully understand and defend
in an interview.

## Limitations
Single-teacher-per-assignment ownership model (no co-teaching), no
malware scanning on uploads, admin role is scoped but not yet built out,
free-tier local storage is not itself durable/replicated (by design — it
is the local stand-in for a cloud object store).

## Future Scope
Admin role and user management, email notifications on grading, real-time
updates (WebSockets) for submission status, plagiarism-detection
integration, and a full React frontend (Option B).

## Conclusion
This project delivers a working, tested, and cloud-architected assignment
portal that can be run for free today and deployed to a real managed
cloud database/storage/auth stack with configuration changes rather than
a rewrite.
