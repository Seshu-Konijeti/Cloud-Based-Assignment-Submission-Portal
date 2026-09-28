"""
routes/assignment_routes.py
ASSIGNMENT MANAGEMENT -- create / read / update / delete.
Only teachers (or admins) may create/update/delete; both roles may read.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from database import db
from models import Assignment, Course
from auth_utils import role_required

assignment_bp = Blueprint("assignments", __name__, url_prefix="/api")


def _parse_deadline(value):
    """Accepts ISO 8601 strings, always interpreted/stored as naive UTC.
    Client-side clocks are never trusted for deadline enforcement --
    see submission_routes.py for the server-side comparison."""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except (ValueError, AttributeError):
        return None


@assignment_bp.route("/assignments", methods=["POST"])
@role_required("teacher", "admin")
def create_assignment():
    data = request.get_json(silent=True) or {}
    course_id = data.get("course_id")
    title = (data.get("title") or "").strip()
    description = data.get("description", "")
    deadline_raw = data.get("deadline")
    max_marks = data.get("max_marks", 100)
    allowed_extensions = data.get("allowed_extensions", "pdf,doc,docx,zip")
    max_file_size_mb = data.get("max_file_size_mb", 10)

    if not course_id or not Course.query.get(course_id):
        return jsonify({"error": "ValidationError", "message": "Valid course_id is required."}), 400
    if not title:
        return jsonify({"error": "ValidationError", "message": "title is required."}), 400
    deadline = _parse_deadline(deadline_raw)
    if not deadline:
        return jsonify({"error": "ValidationError", "message": "deadline must be a valid ISO 8601 datetime."}), 400
    if not isinstance(max_marks, int) or max_marks <= 0:
        return jsonify({"error": "ValidationError", "message": "max_marks must be a positive integer."}), 400

    teacher_id = int(get_jwt_identity())
    assignment = Assignment(
        course_id=course_id,
        title=title,
        description=description,
        deadline=deadline,
        max_marks=max_marks,
        allowed_extensions=allowed_extensions,
        max_file_size_mb=max_file_size_mb,
        created_by=teacher_id,
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({"message": "Assignment created", "assignment": assignment.to_dict()}), 201


@assignment_bp.route("/assignments", methods=["GET"])
@jwt_required()
def get_assignments():
    course_id = request.args.get("course_id", type=int)
    query = Assignment.query
    if course_id:
        query = query.filter_by(course_id=course_id)
    assignments = query.order_by(Assignment.deadline.asc()).all()
    return jsonify({"assignments": [a.to_dict() for a in assignments]}), 200


@assignment_bp.route("/assignments/<int:assignment_id>", methods=["GET"])
@jwt_required()
def get_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "NotFound", "message": "Assignment not found."}), 404
    return jsonify({"assignment": assignment.to_dict()}), 200


@assignment_bp.route("/assignments/<int:assignment_id>", methods=["PUT"])
@role_required("teacher", "admin")
def update_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "NotFound", "message": "Assignment not found."}), 404

    claims = get_jwt()
    if claims.get("role") != "admin" and assignment.created_by != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden", "message": "You may only edit your own assignments."}), 403

    data = request.get_json(silent=True) or {}
    if "title" in data and data["title"].strip():
        assignment.title = data["title"].strip()
    if "description" in data:
        assignment.description = data["description"]
    if "deadline" in data:
        deadline = _parse_deadline(data["deadline"])
        if not deadline:
            return jsonify({"error": "ValidationError", "message": "Invalid deadline."}), 400
        assignment.deadline = deadline
    if "max_marks" in data:
        assignment.max_marks = data["max_marks"]
    if "allowed_extensions" in data:
        assignment.allowed_extensions = data["allowed_extensions"]
    if "max_file_size_mb" in data:
        assignment.max_file_size_mb = data["max_file_size_mb"]

    db.session.commit()
    return jsonify({"message": "Assignment updated", "assignment": assignment.to_dict()}), 200


@assignment_bp.route("/assignments/<int:assignment_id>", methods=["DELETE"])
@role_required("teacher", "admin")
def delete_assignment(assignment_id):
    assignment = Assignment.query.get(assignment_id)
    if not assignment:
        return jsonify({"error": "NotFound", "message": "Assignment not found."}), 404

    claims = get_jwt()
    if claims.get("role") != "admin" and assignment.created_by != int(get_jwt_identity()):
        return jsonify({"error": "Forbidden", "message": "You may only delete your own assignments."}), 403

    db.session.delete(assignment)
    db.session.commit()
    return jsonify({"message": "Assignment deleted"}), 200
