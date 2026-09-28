"""
cloud/auth_service.py

Documents the CLOUD AUTHENTICATION / AUTHORIZATION model. The working
implementation is backend/auth_utils.py + Flask-JWT-Extended.

AUTHENTICATION -- "Who are you?"
- POST /api/register creates a user with a PBKDF2-hashed password.
- POST /api/login verifies credentials and issues a signed JWT
  containing user_id (subject) + role/name/email as custom claims.
- Every protected route requires this JWT via `Authorization: Bearer <token>`.

AUTHORIZATION -- "What are you allowed to do?"
- `role_required("teacher", "admin")` gates teacher-only routes
  (create/update/delete assignment, grade submission, view all
  submissions for an assignment).
- Ownership checks in the route layer additionally stop a STUDENT
  from viewing/downloading/grading another student's submission, and
  stop a TEACHER from editing another teacher's assignment.

SWAPPING TO A MANAGED CLOUD AUTH PROVIDER:
Replace backend/auth_utils.py + auth_routes.py internals with calls to
Firebase Authentication / AWS Cognito / Supabase Auth SDKs. The rest of
the app only needs a decoded {user_id, role} to keep working, so the
route-level RBAC logic does not need to change.
"""
