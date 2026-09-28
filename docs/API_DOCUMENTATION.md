# REST API Documentation

Base URL (local): `http://localhost:5000/api`
Auth: `Authorization: Bearer <access_token>` (obtained from `/login`)

---

## AUTH

### POST /register
- **Auth:** none
- **Body:** `{ "name", "email", "password", "role": "student"|"teacher" }`
- **201:** `{ message, user }`
- **400:** validation error · **409:** email already registered

### POST /login
- **Auth:** none
- **Body:** `{ "email", "password" }`
- **200:** `{ message, access_token, user }`
- **401:** invalid credentials

### POST /logout
- **Auth:** required (any role)
- **200:** `{ message }`

### GET /me
- **Auth:** required
- **200:** `{ user }`

---

## COURSES (supporting resource)

### POST /courses — **Auth:** teacher/admin — creates a course.
### GET /courses — **Auth:** any authenticated user — lists all courses.

---

## ASSIGNMENTS

### POST /assignments
- **Auth:** teacher/admin
- **Body:** `{ course_id, title, description, deadline (ISO 8601), max_marks, allowed_extensions?, max_file_size_mb? }`
- **201:** `{ message, assignment }` · **400/403**

### GET /assignments
- **Auth:** any authenticated user. Optional `?course_id=`.
- **200:** `{ assignments: [...] }`

### GET /assignments/{id}
- **Auth:** any authenticated user
- **200 / 404**

### PUT /assignments/{id}
- **Auth:** teacher/admin, must own the assignment
- **200 / 403 (not owner) / 404**

### DELETE /assignments/{id}
- **Auth:** teacher/admin, must own the assignment
- **200 / 403 / 404**

---

## SUBMISSIONS

### POST /assignments/{id}/submit
- **Auth:** student
- **Body:** multipart/form-data, field `file`
- **201:** `{ message, submission }` (status `SUBMITTED` or `LATE`)
- **400:** bad extension / no file · **403:** deadline passed & late submissions disabled · **409:** duplicate & resubmission disabled

### GET /submissions/me
- **Auth:** student — **200:** `{ submissions: [...] }` (their own only)

### GET /assignments/{id}/submissions
- **Auth:** teacher/admin — **200:** all submissions for that assignment, with student name/email attached

### GET /submissions/{id}
- **Auth:** any authenticated user, but a student may only fetch **their own**
- **200 / 403 / 404**

### GET /submissions/{id}/download
- **Auth:** same ownership rule as above — streams the file
- **200 (file) / 403 / 404**

---

## FEEDBACK / GRADING

### POST /submissions/{id}/grade
- **Auth:** teacher/admin
- **Body:** `{ marks: number, feedback: string }`
- **200:** `{ message, submission }` (status becomes `GRADED`)
- **400:** marks out of range · **403:** not a teacher

### GET /submissions/{id}/feedback
- **Auth:** owner student or teacher/admin
- **200:** `{ marks, feedback, graded_at, submission_status }`

---

## DASHBOARDS

### GET /dashboard/student — **Auth:** student — aggregate counts + upcoming deadlines + recent feedback
### GET /dashboard/teacher — **Auth:** teacher/admin — aggregate counts + upcoming deadlines + recent uploads

---

## Common HTTP status codes used
| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Resource created |
| 400 | Validation error |
| 401 | Not authenticated / bad credentials |
| 403 | Authenticated but not authorized (wrong role or not the owner) |
| 404 | Resource not found |
| 409 | Conflict (duplicate email / duplicate submission) |
| 413 | File too large |
| 500 | Unexpected server error |
