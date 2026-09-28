# Cloud Security

## Implemented in this project
- **Authentication** — JWT issued at login, required on every protected route.
- **Authorization / RBAC** — `role_required()` decorator + per-object ownership
  checks (a student can only see/download/grade-feedback their own submission;
  a teacher can only edit their own assignments).
- **Password hashing** — PBKDF2 via Werkzeug's `generate_password_hash`;
  plaintext passwords are never stored or logged.
- **File-type validation** — extension allow-list per assignment (`allowed_extensions`).
- **File-size validation** — `MAX_CONTENT_LENGTH` enforced by Flask, returns `413`.
- **Environment variables & secrets management** — every credential/secret is
  read from `.env` (see `.env.example`), never hardcoded, and `.env` is
  git-ignored.
- **CORS** — configurable allow-list (`CORS_ORIGINS`), defaults to `*` only
  for local development.
- **Input validation** — every route validates required fields, types, and
  ranges (e.g. marks cannot exceed `max_marks`) before touching the database.
- **Storage isolation** — files are namespaced per assignment/student folder
  with UUID-prefixed names, preventing path guessing/overwriting.
- **Consistent error responses** — no stack traces or internal details ever
  reach the client; global error handlers return generic JSON messages.

## What a production deployment would add
- **HTTPS everywhere** — terminated at the load balancer / platform edge.
- **Encryption at rest** — enabled by default on managed cloud DB/storage
  (RDS, S3, Firestore, Firebase Storage all encrypt at rest).
- **Encryption in transit** — TLS between every hop (client → API Gateway →
  backend → DB/storage).
- **Signed URLs** — for direct-to-client file downloads without proxying
  bytes through the backend, with a short expiry.
- **Rate limiting** — e.g. `Flask-Limiter` or an API Gateway throttling
  policy, to blunt brute-force login attempts and abusive upload bursts.
- **Malware scanning** — pass uploaded files through a scanning service
  (e.g. ClamAV, or a cloud provider's file-scan integration) before they are
  ever served back to a teacher.
- **Audit logs** — a separate append-only log of who graded what and when,
  distinct from ordinary application logs.
- **Database & storage IAM permissions** — least-privilege service accounts
  (the backend's DB user can't drop tables; its storage credentials are
  scoped to one bucket/prefix).
- **Automated backups** — daily snapshots with a retention policy on the
  managed database and versioning enabled on the object store.

## Common mistakes students should avoid
- Hardcoding secrets/API keys directly in source files that get pushed to GitHub.
- Trusting the client's uploaded filename as the storage path (path traversal risk).
- Trusting a client-supplied timestamp for deadline enforcement.
- Returning raw exception messages/stack traces to the frontend.
- Storing plaintext passwords "just for the demo" — never do this, even in student projects.
- Leaving `CORS_ORIGINS=*` and debug mode on in a real deployment.
- Giving every authenticated user access to every record instead of checking ownership.
