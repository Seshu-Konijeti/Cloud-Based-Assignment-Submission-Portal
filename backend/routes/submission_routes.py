"""
routes/submission_routes.py
SUBMISSION SYSTEM: upload, list-own, list-for-assignment (teacher),
download, deadline enforcement, resubmission, and FEEDBACK/GRADING.

Workflow implemented here:
  Select Assignment -> Validate File -> Upload to Object Storage
  -> Save Submission Metadata -> Confirmation
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from database import db
from models import Assignment, Submission, User
from storage_service import LocalStorageService, allowed_file
from auth_utils import role_required

submission_bp = Blueprint("submissions", __name__, url_prefix="/api")


def get_storage():
    return LocalStorageService(current_app.config["LOCAL_STORAGE_ROOT"])


@submission_bp.route("/assignments/<int:assignment_id>/submit", methods=["POST"])
@role_required("student")
def submit_assignment(assignment_id):
    student_id = int(get_jwt_identity())
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "NotFound", "message": "Assignment does not exist."}), 404

    if "file" not in request.files:
        return jsonify({"error": "ValidationError", "message": "No file part in the request."}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "ValidationError", "message": "No file selected."}), 400

    allowed_ext = set(e.strip().lower() for e in assignment.allowed_extensions.split(","))
    if not allowed_file(file.filename, allowed_ext):
        return jsonify({
            "error": "ValidationError",
            "message": f"File type not allowed. Allowed types: {sorted(allowed_ext)}"
        }), 400

    # --- Duplicate / resubmission policy ---
    existing = Submission.query.filter_by(assignment_id=assignment_id, student_id=student_id).first()
    if existing and not current_app.config["ALLOW_RESUBMISSION"]:
        return jsonify({
            "error": "Conflict",
            "message": "You have already submitted this assignment and resubmission is not allowed."
        }), 409

    storage = get_storage()
    storage_path, original_name = storage.save_file(file, assignment_id, student_id)

    # --- Server-side deadline check (never trust client clocks) ---
    now = datetime.utcnow()
    if now > assignment.deadline:
        if not current_app.config["ALLOW_LATE_SUBMISSION"]:
            storage.delete_file(storage_path)  # roll back the upload
            return jsonify({"error": "Forbidden", "message": "The deadline has passed. Late submissions are disabled."}), 403
        status = "LATE"
    else:
        status = "SUBMITTED"

    if existing:
        # Resubmission: remove old file, update the same metadata row.
        storage.delete_file(existing.storage_path)
        existing.file_name = original_name
        existing.storage_path = storage_path
        existing.submitted_at = now
        existing.submission_status = status
        existing.attempt_number = (existing.attempt_number or 1) + 1
        existing.marks = None
        existing.feedback = None
        existing.graded_at = None
        db.session.commit()
        submission = existing
    else:
        submission = Submission(
            assignment_id=assignment_id,
            student_id=student_id,
            file_name=original_name,
            storage_path=storage_path,
            submitted_at=now,
            submission_status=status,
        )
        db.session.add(submission)
        db.session.commit()

    return jsonify({"message": "Submission received", "submission": submission.to_dict()}), 201


@submission_bp.route("/submissions/me", methods=["GET"])
@role_required("student")
def my_submissions():
    student_id = int(get_jwt_identity())
    subs = Submission.query.filter_by(student_id=student_id).order_by(Submission.submitted_at.desc()).all()
    return jsonify({"submissions": [s.to_dict() for s in subs]}), 200


@submission_bp.route("/assignments/<int:assignment_id>/submissions", methods=["GET"])
@role_required("teacher", "admin")
def submissions_for_assignment(assignment_id):
    if not Assignment.query.get(assignment_id):
        return jsonify({"error": "NotFound", "message": "Assignment not found."}), 404
    subs = Submission.query.filter_by(assignment_id=assignment_id).order_by(Submission.submitted_at.desc()).all()
    result = []
    for s in subs:
        d = s.to_dict()
        student = User.query.get(s.student_id)
        d["student_name"] = student.name if student else "Unknown"
        d["student_email"] = student.email if student else None
        result.append(d)
    return jsonify({"submissions": result}), 200


@submission_bp.route("/submissions/<int:submission_id>", methods=["GET"])
@jwt_required()
def get_submission(submission_id):
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "NotFound", "message": "Submission not found."}), 404

    claims = get_jwt()
    user_id = int(get_jwt_identity())
    # Authorization: a student may only view their OWN submission.
    if claims.get("role") == "student" and submission.student_id != user_id:
        return jsonify({"error": "Forbidden", "message": "You cannot view another student's submission."}), 403

    return jsonify({"submission": submission.to_dict()}), 200


@submission_bp.route("/submissions/<int:submission_id>/download", methods=["GET"])
@jwt_required()
def download_submission(submission_id):
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "NotFound", "message": "Submission not found."}), 404

    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") == "student" and submission.student_id != user_id:
        return jsonify({"error": "Forbidden", "message": "You cannot download another student's file."}), 403

    storage = get_storage()
    if not storage.file_exists(submission.storage_path):
        return jsonify({"error": "NotFound", "message": "File missing from storage."}), 404

    full_path = storage.get_absolute_path(submission.storage_path)
    return send_file(full_path, as_attachment=True, download_name=submission.file_name)


@submission_bp.route("/submissions/<int:submission_id>/grade", methods=["POST"])
@role_required("teacher", "admin")
def grade_submission(submission_id):
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "NotFound", "message": "Submission not found."}), 404

    assignment = Assignment.query.get(submission.assignment_id)
    data = request.get_json(silent=True) or {}
    marks = data.get("marks")
    feedback = data.get("feedback", "")

    if marks is None or not isinstance(marks, (int, float)):
        return jsonify({"error": "ValidationError", "message": "marks (number) is required."}), 400
    if marks < 0 or marks > assignment.max_marks:
        return jsonify({
            "error": "ValidationError",
            "message": f"marks must be between 0 and {assignment.max_marks}."
        }), 400

    submission.marks = marks
    submission.feedback = feedback
    submission.graded_at = datetime.utcnow()
    submission.graded_by = int(get_jwt_identity())
    submission.submission_status = "GRADED"
    db.session.commit()

    return jsonify({"message": "Submission graded", "submission": submission.to_dict()}), 200


@submission_bp.route("/submissions/<int:submission_id>/feedback", methods=["GET"])
@jwt_required()
def get_feedback(submission_id):
    submission = Submission.query.get(submission_id)
    if not submission:
        return jsonify({"error": "NotFound", "message": "Submission not found."}), 404

    claims = get_jwt()
    user_id = int(get_jwt_identity())
    if claims.get("role") == "student" and submission.student_id != user_id:
        return jsonify({"error": "Forbidden", "message": "You cannot view another student's feedback."}), 403

    return jsonify({
        "marks": submission.marks,
        "feedback": submission.feedback,
        "graded_at": submission.graded_at.isoformat() if submission.graded_at else None,
        "submission_status": submission.submission_status,
    }), 200
