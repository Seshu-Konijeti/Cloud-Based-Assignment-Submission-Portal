"""
seed.py
Populates the database with DUMMY teachers, students, a course and an
assignment so the app can be demoed immediately after setup.

Run:
    python seed.py
"""
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

from app import create_app
from database import db
from models import User, Course, Assignment

app = create_app()

with app.app_context():
    if User.query.filter_by(email="teacher@example.com").first():
        print("Seed data already present. Skipping.")
    else:
        teacher = User(
            name="Dr. Asha Rao",
            email="teacher@example.com",
            password_hash=generate_password_hash("Teacher@123"),
            role="teacher",
        )
        student1 = User(
            name="Rahul Sharma",
            email="student1@example.com",
            password_hash=generate_password_hash("Student@123"),
            role="student",
        )
        student2 = User(
            name="Priya Nair",
            email="student2@example.com",
            password_hash=generate_password_hash("Student@123"),
            role="student",
        )
        db.session.add_all([teacher, student1, student2])
        db.session.commit()

        course = Course(course_name="Cloud Computing 101", teacher_id=teacher.user_id)
        db.session.add(course)
        db.session.commit()

        assignment = Assignment(
            course_id=course.course_id,
            title="Assignment 1: Cloud Storage Basics",
            description="Write a short report comparing object storage and block storage.",
            deadline=datetime.utcnow() + timedelta(days=7),
            max_marks=100,
            allowed_extensions="pdf,doc,docx,zip",
            max_file_size_mb=10,
            created_by=teacher.user_id,
        )
        db.session.add(assignment)
        db.session.commit()

        print("Seed data created:")
        print("  Teacher login -> teacher@example.com / Teacher@123")
        print("  Student login -> student1@example.com / Student@123")
        print("  Student login -> student2@example.com / Student@123")
        print(f"  Course: {course.course_name} (id={course.course_id})")
        print(f"  Assignment: {assignment.title} (id={assignment.assignment_id})")
