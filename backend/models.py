"""
models.py
Database MODELS (metadata only). Actual assignment files never live
here -- they live in cloud object storage (see storage_service.py).
Only the storage_path / file_url reference is stored, which is the
standard cloud-architecture pattern: DB for metadata, Object Storage
for blobs.
"""
from datetime import datetime
from database import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # "student" | "teacher" | "admin"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship("Assignment", backref="course", lazy=True)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "teacher_id": self.teacher_id,
            "created_at": self.created_at.isoformat(),
        }


class Assignment(db.Model):
    __tablename__ = "assignments"

    assignment_id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False)  # always stored in UTC
    max_marks = db.Column(db.Integer, nullable=False, default=100)
    allowed_extensions = db.Column(db.String(120), nullable=False, default="pdf,doc,docx,zip")
    max_file_size_mb = db.Column(db.Integer, nullable=False, default=10)
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship("Submission", backref="assignment", lazy=True)

    def to_dict(self):
        return {
            "assignment_id": self.assignment_id,
            "course_id": self.course_id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.isoformat(),
            "max_marks": self.max_marks,
            "allowed_extensions": self.allowed_extensions,
            "max_file_size_mb": self.max_file_size_mb,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }


class Submission(db.Model):
    __tablename__ = "submissions"

    submission_id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignments.assignment_id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    file_name = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(500), nullable=False)  # object-storage key/path
    file_url = db.Column(db.String(500), nullable=True)  # signed/public URL if applicable

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    submission_status = db.Column(db.String(20), default="SUBMITTED")  # SUBMITTED|LATE|GRADED
    attempt_number = db.Column(db.Integer, default=1)

    marks = db.Column(db.Integer, nullable=True)
    feedback = db.Column(db.Text, nullable=True)
    graded_at = db.Column(db.DateTime, nullable=True)
    graded_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=True)

    __table_args__ = (
        db.Index("idx_assignment_student", "assignment_id", "student_id"),
    )

    def to_dict(self):
        return {
            "submission_id": self.submission_id,
            "assignment_id": self.assignment_id,
            "student_id": self.student_id,
            "file_name": self.file_name,
            "storage_path": self.storage_path,
            "submitted_at": self.submitted_at.isoformat(),
            "submission_status": self.submission_status,
            "attempt_number": self.attempt_number,
            "marks": self.marks,
            "feedback": self.feedback,
            "graded_at": self.graded_at.isoformat() if self.graded_at else None,
        }
