"""
cloud/storage_service.py

This file documents the CLOUD OBJECT STORAGE abstraction. The working
implementation is backend/storage_service.py::LocalStorageService, which
mimics an S3/Firebase-Storage-style API:

    save_file(file, assignment_id, student_id) -> (storage_path, original_name)
    get_absolute_path(storage_path)            -> local path (would be a signed URL in prod)
    delete_file(storage_path)
    file_exists(storage_path)

TO SWAP IN A REAL CLOUD PROVIDER:
Implement an S3StorageService (boto3) or FirebaseStorageService
(firebase-admin) with the SAME four methods, then change one factory
function (`get_storage()` in routes/submission_routes.py) to
instantiate it based on `STORAGE_BACKEND` in config.py. Every route
that uploads/downloads/deletes files is otherwise untouched.

STORAGE LAYOUT (object "key" convention, mirrors S3 prefixes):
    assignments/
        assignment_<id>/
            student_<id>/
                <uuid>_<original_filename>

WHY UUID-PREFIXED NAMES:
- Prevents filename collisions across students/attempts.
- Prevents a student from guessing another student's object key.
- Mirrors the real-world practice of never trusting client-supplied
  filenames as storage keys.

ACCESS CONTROL MODEL:
- A student may only fetch objects under their own student_<id> folder.
  This is enforced in the route layer (submission ownership check),
  the same job an S3 bucket policy or Firebase Storage security rule
  would do in a real cloud deployment.
"""
