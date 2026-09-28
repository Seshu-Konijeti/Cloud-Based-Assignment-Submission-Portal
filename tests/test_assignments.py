"""
Test cases 6-7 and role-authorization for assignment CRUD.
"""
from datetime import datetime, timedelta
from conftest import auth_header


def create_course_and_assignment(client, teacher_token, deadline_delta=timedelta(days=3)):
    token, _ = teacher_token
    course_res = client.post("/api/courses", json={"course_name": "Cloud 101"}, headers=auth_header(token))
    course_id = course_res.get_json()["course"]["course_id"]
    deadline = (datetime.utcnow() + deadline_delta).isoformat()
    a_res = client.post("/api/assignments", json={
        "course_id": course_id, "title": "Assignment 1", "description": "desc",
        "deadline": deadline, "max_marks": 100
    }, headers=auth_header(token))
    return a_res


def test_teacher_creates_assignment(client, teacher_token):
    res = create_course_and_assignment(client, teacher_token)
    assert res.status_code == 201
    assert res.get_json()["assignment"]["title"] == "Assignment 1"


def test_student_cannot_create_assignment(client, student_token):
    token, _ = student_token
    res = client.post("/api/assignments", json={
        "course_id": 1, "title": "Hack", "deadline": datetime.utcnow().isoformat(), "max_marks": 100
    }, headers=auth_header(token))
    assert res.status_code == 403


def test_student_can_view_assignments(client, teacher_token, student_token):
    create_course_and_assignment(client, teacher_token)
    token, _ = student_token
    res = client.get("/api/assignments", headers=auth_header(token))
    assert res.status_code == 200
    assert len(res.get_json()["assignments"]) == 1
