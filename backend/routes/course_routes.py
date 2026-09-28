"""
routes/course_routes.py
Minimal course management so assignments have something to belong to.
Kept intentionally small -- courses are not the focus of this project.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db
from models import Course
from auth_utils import role_required

course_bp = Blueprint("courses", __name__, url_prefix="/api")


@course_bp.route("/courses", methods=["POST"])
@role_required("teacher", "admin")
def create_course():
    data = request.get_json(silent=True) or {}
    name = (data.get("course_name") or "").strip()
    if not name:
        return jsonify({"error": "ValidationError", "message": "course_name is required."}), 400

    teacher_id = int(get_jwt_identity())
    course = Course(course_name=name, teacher_id=teacher_id)
    db.session.add(course)
    db.session.commit()
    return jsonify({"message": "Course created", "course": course.to_dict()}), 201


@course_bp.route("/courses", methods=["GET"])
@jwt_required()
def list_courses():
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return jsonify({"courses": [c.to_dict() for c in courses]}), 200
