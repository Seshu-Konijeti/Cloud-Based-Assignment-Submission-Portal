"""
routes/dashboard_routes.py
Aggregated STUDENT and TEACHER dashboard queries.
"""
from datetime import datetime
from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity

from models import Assignment, Submission, Course, User
from auth_utils import role_required

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/dashboard")


@dashboard_bp.route("/student", methods=["GET"])
@role_required("student")
def student_dashboard():
    student_id = int(get_jwt_identity())
    user = User.query.get(student_id)

    all_assignments = Assignment.query.all()
    my_subs = {s.assignment_id: s for s in Submission.query.filter_by(student_id=student_id).all()}

    total = len(all_assignments)
    submitted = sum(1 for s in my_subs.values() if s.submission_status in ("SUBMITTED", "LATE", "GRADED"))
    late = sum(1 for s in my_subs.values() if s.submission_status == "LATE")
    graded = sum(1 for s in my_subs.values() if s.submission_status == "GRADED")
    pending = total - len(my_subs)

    now = datetime.utcnow()
    upcoming = sorted(
        [a for a in all_assignments if a.assignment_id not in my_subs and a.deadline > now],
        key=lambda a: a.deadline,
    )[:5]

    recent_feedback = sorted(
        [s for s in my_subs.values() if s.submission_status == "GRADED"],
        key=lambda s: s.graded_at or now, reverse=True,
    )[:5]

    return jsonify({
        "welcome": f"Welcome, {user.name}",
        "total_assignments": total,
        "pending_assignments": pending,
        "submitted_assignments": submitted,
        "late_assignments": late,
        "graded_assignments": graded,
        "upcoming_deadlines": [a.to_dict() for a in upcoming],
        "recent_feedback": [s.to_dict() for s in recent_feedback],
    }), 200


@dashboard_bp.route("/teacher", methods=["GET"])
@role_required("teacher", "admin")
def teacher_dashboard():
    teacher_id = int(get_jwt_identity())
    my_courses = Course.query.filter_by(teacher_id=teacher_id).all()
    course_ids = [c.course_id for c in my_courses]
    my_assignments = Assignment.query.filter(Assignment.course_id.in_(course_ids)).all() if course_ids else []
    assignment_ids = [a.assignment_id for a in my_assignments]

    all_subs = Submission.query.filter(Submission.assignment_id.in_(assignment_ids)).all() if assignment_ids else []
    total_students = User.query.filter_by(role="student").count()

    pending_review = sum(1 for s in all_subs if s.submission_status in ("SUBMITTED", "LATE"))
    late = sum(1 for s in all_subs if s.submission_status == "LATE")
    graded = sum(1 for s in all_subs if s.submission_status == "GRADED")

    now = datetime.utcnow()
    upcoming = sorted([a for a in my_assignments if a.deadline > now], key=lambda a: a.deadline)[:5]
    recent_uploads = sorted(all_subs, key=lambda s: s.submitted_at, reverse=True)[:5]

    return jsonify({
        "total_assignments": len(my_assignments),
        "total_students": total_students,
        "total_submissions": len(all_subs),
        "pending_reviews": pending_review,
        "late_submissions": late,
        "graded_submissions": graded,
        "recent_uploads": [s.to_dict() for s in recent_uploads],
        "upcoming_deadlines": [a.to_dict() for a in upcoming],
    }), 200
