# Interview Preparation — 10 Questions & Answers

**1. Explain your project.**
It's a cloud-based assignment portal. Teachers create assignments with a
deadline and a maximum mark; students upload their submission file, which
gets validated for type and size and time-stamped on the server, not the
client. The metadata — who submitted what, when, their marks and
feedback — lives in a relational database, while the actual file bytes
live in a separate object-storage layer, which mirrors how real cloud
platforms like S3 or Firebase Storage work. Teachers grade submissions
through a REST API that's locked down with JWT authentication and
role-based access control, so a student can never see another student's
submission or grades.

**2. Why did you separate the database from the file storage instead of just storing files in the database?**
Databases are optimized for structured, relatively small rows and fast
queries; they perform and scale poorly with large binary blobs. Object
storage is purpose-built for exactly that — cheap, effectively unlimited
capacity, and it doesn't compete with your database's compute for every
file read. I only store a `storage_path` reference in the database, never
the file bytes themselves.

**3. How does your object storage abstraction work, and how would you swap it for AWS S3?**
`storage_service.py` exposes four methods — `save_file`,
`get_absolute_path`, `delete_file`, `file_exists` — behind a
`LocalStorageService` class that currently writes to disk. Every route
only calls those four methods, so swapping in an `S3StorageService`
(using boto3) that implements the same interface requires changing one
factory function, not the routes themselves.

**4. Walk me through your authentication and authorization.**
Authentication answers "who are you?" — a user logs in with email and
password, I verify the password hash, and issue a signed JWT containing
their user ID and role. Authorization answers "what can you do?" — every
protected route either requires a specific role (`role_required("teacher")`)
or additionally checks object ownership, like confirming a submission
belongs to the requesting student before letting them download it.

**5. How do you design your REST APIs?**
Resource-oriented URLs (`/assignments/{id}/submissions`), HTTP verbs
mapped to CRUD actions, JSON request/response bodies, and consistent
status codes — 400 for validation errors, 401 for missing/invalid auth,
403 for authorization failures, 404 for missing resources, 409 for
conflicts like duplicate submissions.

**6. How do you handle file uploads securely?**
I validate the extension against an allow-list configured per assignment,
enforce a maximum file size via Flask's `MAX_CONTENT_LENGTH`, and rename
every uploaded file with a UUID prefix so a student can't guess or
overwrite another student's storage path.

**7. How would this scale to 100,000 students submitting near a deadline?**
Move off SQLite onto a managed database with connection pooling, move file
storage onto S3 (which handles massive concurrent writes natively), put a
load balancer with autoscaling in front of multiple backend instances, and
push any slow post-processing (like malware scanning) onto a background
queue so the upload response itself stays fast.

**8. What security measures does your project implement, and what would you add for production?**
Implemented: password hashing, JWT auth, RBAC, input validation, file-type
and size validation, environment-variable secrets, CORS configuration. For
production I'd add HTTPS termination, encryption at rest (handled
automatically by managed cloud DB/storage), signed URLs for direct
downloads, rate limiting on login, and malware scanning on uploads.

**9. How did you handle deadlines and late submissions?**
The deadline is stored in UTC and compared against `datetime.utcnow()` on
the server at the moment of upload — I never trust a timestamp sent by the
client, because it's trivial to fake. If the submission arrives after the
deadline, the status is set to `LATE` rather than `SUBMITTED`, and I made
whether late submissions are even allowed a configurable environment
variable.

**10. How did you test this project, and what would you still want to add?**
24 automated pytest cases cover registration, login, role-based dashboard
access, assignment CRUD authorization, valid/invalid file uploads,
on-time/late/resubmission status logic, cross-student authorization
denial, and grading validation (including rejecting marks above the
maximum). I'd still want to add tests simulating storage/database outages
and an end-to-end browser test with something like Playwright.
