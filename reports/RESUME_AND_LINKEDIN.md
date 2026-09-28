# Resume / LinkedIn / GitHub Proof

## A. Resume Bullet Points
- Designed and built a cloud-oriented assignment submission platform in
  Flask, separating metadata (relational database) from file storage
  (object-storage abstraction), with a documented migration path to
  AWS S3/RDS or Firebase.
- Implemented JWT-based authentication and role-based access control
  (RBAC) across 20+ REST endpoints, enforcing per-object ownership checks
  so students can never access another student's submissions or grades.
- Wrote 24 automated pytest test cases covering authentication,
  authorization, deadline enforcement, and grading validation, achieving a
  fully passing CI-ready test suite.

## B. 2-Line Resume Project Description
Cloud-Based Student Assignment Submission & Feedback Portal — a Flask/REST
API platform with JWT auth, role-based access control, cloud-storage
abstraction, and deadline-aware submission/grading workflows, fully tested
with pytest.

## C. LinkedIn Project Description
Built a full-stack cloud computing project simulating a real EdTech
assignment portal: teachers create assignments with deadlines, students
upload submissions to an object-storage layer while metadata lives in a
relational database, and grading/feedback flows back through a
role-based REST API. Designed the storage and database layers as
swappable interfaces so the same codebase can run entirely free/local or
be pointed at managed cloud services (S3/RDS, Firebase, Supabase) with a
configuration change — no rewrite required. Covered with 24 automated
tests.

## D. Technical Skills Demonstrated
Python (Flask), REST API design, JWT authentication, role-based
authorization, relational database design (SQLAlchemy), cloud
object-storage architecture, environment-variable-based secrets
management, automated testing (pytest), Git/GitHub workflow, cloud
deployment planning (AWS/Azure/GCP + free-tier PaaS).

## E. GitHub Project Description
A cloud-computing course project implementing a role-based student
assignment submission and feedback portal: JWT authentication, RBAC,
deadline-aware submission workflow, teacher grading/feedback, a
cloud-object-storage abstraction layer ready to swap for S3/Firebase, and
a fully passing pytest suite.
