"""
storage_service.py
Cloud OBJECT STORAGE abstraction.

Why a separate service instead of saving files straight in a route?
Because in production you would swap LocalStorageService for
S3StorageService / FirebaseStorageService / SupabaseStorageService
WITHOUT changing a single line of route code -- every route only calls
the three methods below (save, get_path_or_url, delete).

Storage layout (mirrors the brief given in the spec):
    storage/assignments/<assignment_id>/<student_id>/<unique_filename>

This keeps every student's submissions isolated by folder, which is also
how per-object access permissions would be modeled in S3 (IAM policy per
prefix) or Firebase Storage (security rules per path).
"""
import os
import uuid
from werkzeug.utils import secure_filename


class LocalStorageService:
    """Free-tier / local-dev stand-in for a cloud object store."""

    def __init__(self, root_path):
        self.root_path = root_path
        os.makedirs(self.root_path, exist_ok=True)

    def _folder_for(self, assignment_id, student_id):
        folder = os.path.join(self.root_path, f"assignment_{assignment_id}", f"student_{student_id}")
        os.makedirs(folder, exist_ok=True)
        return folder

    def save_file(self, file_storage, assignment_id, student_id):
        """Saves an uploaded file and returns (storage_path, unique_filename).
        A UUID prefix prevents filename collisions and prevents students
        from guessing/overwriting each other's object keys."""
        original_name = secure_filename(file_storage.filename)
        unique_name = f"{uuid.uuid4().hex}_{original_name}"
        folder = self._folder_for(assignment_id, student_id)
        full_path = os.path.join(folder, unique_name)
        file_storage.save(full_path)
        # storage_path is what we persist in the DB -- a relative "object key",
        # exactly like an S3 key, NOT an absolute filesystem path.
        storage_path = os.path.relpath(full_path, self.root_path)
        return storage_path, original_name

    def get_absolute_path(self, storage_path):
        """Resolves a stored object key back to a real path for download.
        In an S3 backend this would instead generate a signed URL."""
        return os.path.join(self.root_path, storage_path)

    def delete_file(self, storage_path):
        full_path = self.get_absolute_path(storage_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

    def file_exists(self, storage_path):
        return os.path.exists(self.get_absolute_path(storage_path))


def allowed_file(filename, allowed_extensions):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1].lower()
    return ext in allowed_extensions
