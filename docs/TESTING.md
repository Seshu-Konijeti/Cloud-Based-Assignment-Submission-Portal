# Testing Strategy

Automated tests live in `tests/` (pytest) and currently cover 24 cases,
all passing. Run with:
```
pytest
```

| Test ID | Scenario | Automated? |
|---|---|---|
| T1 | Student registration | ✅ `test_auth.py` |
| T2 | Teacher login (valid) | ✅ |
| T3 | Invalid login | ✅ |
| T4 | Student dashboard authorization (teacher blocked) | ✅ |
| T5 | Teacher dashboard authorization (student blocked) | ✅ |
| T6 | Teacher creates assignment | ✅ `test_assignments.py` |
| T7 | Student views assignment | ✅ |
| T8 | Valid file upload | ✅ `test_submissions.py` |
| T9 | Invalid file extension rejected | ✅ |
| T10 | Oversized file | Manual (set `MAX_FILE_SIZE_MB=0` to reproduce a 413) |
| T11 | On-time submission | ✅ (implied by T8 status) |
| T12 | Late submission | ✅ |
| T13 | Resubmission | ✅ |
| T14 | Student views own submission | ✅ |
| T15 | Student cannot view another student's submission | ✅ |
| T16 | Teacher views submissions | ✅ |
| T17 | Teacher grades submission | ✅ |
| T18 | Marks above maximum rejected | ✅ |
| T19 | Student views feedback | ✅ |
| T20 | Unauthorized grading rejected | ✅ |
| T21 | File retrieval (download) | ✅ |
| T22 | Cloud-storage failure | Manual: point `LOCAL_STORAGE_ROOT` at a read-only path |
| T23 | Database failure | Manual: point `DATABASE_URL` at an unreachable host |
| T24 | Logout | ✅ `test_auth.py` |
| T25 | Protected route requires token | ✅ |
| T26 | Duplicate registration rejected | ✅ |

Every automated test asserts both the **HTTP status code** and, where
relevant, the **response body shape** — not just "it didn't crash".
