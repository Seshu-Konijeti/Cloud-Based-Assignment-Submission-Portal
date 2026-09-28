# Database Design

## Entity Relationship
```
User (teacher) --1:N--> Course --1:N--> Assignment --1:N--> Submission <--N:1-- User (student)
```

## Tables

### users
| Field | Type | Notes |
|---|---|---|
| user_id | PK, int | |
| name | string | |
| email | string, unique, indexed | login identifier |
| password_hash | string | PBKDF2 hash, never plaintext |
| role | string | `student` \| `teacher` \| `admin` |
| created_at | datetime | |

### courses
| course_id | PK |
| course_name | string |
| teacher_id | FK -> users.user_id |
| created_at | datetime |

### assignments
| assignment_id | PK |
| course_id | FK -> courses.course_id |
| title, description | |
| deadline | datetime (UTC) |
| max_marks | int |
| allowed_extensions | string, e.g. "pdf,docx,zip" |
| max_file_size_mb | int |
| created_by | FK -> users.user_id |
| created_at | datetime |

### submissions
| submission_id | PK |
| assignment_id | FK -> assignments.assignment_id |
| student_id | FK -> users.user_id |
| file_name | string (original name, for display) |
| storage_path | string (object-storage key, NOT a DB blob) |
| submitted_at | datetime |
| submission_status | `SUBMITTED` \| `LATE` \| `GRADED` |
| attempt_number | int, increments on resubmission |
| marks | int, nullable until graded |
| feedback | text, nullable until graded |
| graded_at | datetime, nullable |
| graded_by | FK -> users.user_id, nullable |

Composite index on `(assignment_id, student_id)` — this is the pair almost
every query filters or joins on (one student's row for one assignment), so
it is indexed rather than left to a full table scan.

## Why files are NOT stored as DB blobs
1. **Cost & performance** — cloud databases charge/perform far worse for
   large binary rows than object stores designed for exactly that (S3,
   Firebase Storage). Every read of a row would otherwise drag megabytes of
   file bytes through the DB connection even when only metadata is needed.
2. **Scalability** — object storage scales storage capacity independently of
   database compute/IOPS; a spike of 100,000 PDF uploads doesn't touch DB
   performance at all.
3. **Streaming** — object stores serve files directly (or via signed URL),
   so downloads don't route through the application server's memory.
4. **Backup/versioning** — S3-style storage has native versioning/lifecycle
   rules; you would not want that logic bolted onto a relational database.

## Cloud Database Queries (examples used by this project)
- Student dashboard: `Submission.query.filter_by(student_id=...)` joined in
  Python against all `Assignment` rows to compute pending/late/graded counts.
- Teacher dashboard: `Submission.query.filter(Submission.assignment_id.in_(...))`
  scoped to only the teacher's own courses/assignments.
- Grading: a single row update — `submission.marks`, `.feedback`,
  `.graded_at`, `.submission_status` — never touches the file itself.
