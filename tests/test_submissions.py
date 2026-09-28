"""
Test cases 8-21 from the spec: file upload/validation, deadline logic,
resubmission, ownership authorization, grading validation.
"""
import io
from datetime import datetime, timedelta
from conftest import auth_header
from test_assignments import create_course_and_assignment


def upload(client, token, assignment_id, filename="report.pdf", content=b"%PDF-1.4 dummy"):
    data = {"file": (io.BytesIO(content), filename)}
    return client.post(
        f"/api/assignments/{assignment_id}/submit",
        data=data, headers=auth_header(token), content_type="multipart/form-data"
    )


def test_valid_pdf_upload(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    res = upload(client, s_token, a["assignment_id"])
    assert res.status_code == 201
    assert res.get_json()["submission"]["submission_status"] == "SUBMITTED"


def test_invalid_file_extension_rejected(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    res = upload(client, s_token, a["assignment_id"], filename="virus.exe")
    assert res.status_code == 400


def test_late_submission_flagged(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token, deadline_delta=timedelta(seconds=-5)).get_json()["assignment"]
    s_token, _ = student_token
    res = upload(client, s_token, a["assignment_id"])
    assert res.status_code == 201
    assert res.get_json()["submission"]["submission_status"] == "LATE"


def test_resubmission_updates_same_record(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    first = upload(client, s_token, a["assignment_id"], filename="v1.pdf").get_json()["submission"]
    second = upload(client, s_token, a["assignment_id"], filename="v2.pdf").get_json()["submission"]
    assert first["submission_id"] == second["submission_id"]
    assert second["attempt_number"] == 2
    assert second["file_name"] == "v2.pdf"


def test_student_cannot_view_another_students_submission(client, teacher_token, student_token, another_student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s1_token, _ = student_token
    s2_token, _ = another_student_token
    sub = upload(client, s1_token, a["assignment_id"]).get_json()["submission"]
    res = client.get(f"/api/submissions/{sub['submission_id']}", headers=auth_header(s2_token))
    assert res.status_code == 403


def test_teacher_views_submissions_for_assignment(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    upload(client, s_token, a["assignment_id"])
    t_token, _ = teacher_token
    res = client.get(f"/api/assignments/{a['assignment_id']}/submissions", headers=auth_header(t_token))
    assert res.status_code == 200
    assert len(res.get_json()["submissions"]) == 1


def test_teacher_grades_submission(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    sub = upload(client, s_token, a["assignment_id"]).get_json()["submission"]
    t_token, _ = teacher_token
    res = client.post(f"/api/submissions/{sub['submission_id']}/grade",
                       json={"marks": 85, "feedback": "Good work"}, headers=auth_header(t_token))
    assert res.status_code == 200
    assert res.get_json()["submission"]["submission_status"] == "GRADED"


def test_marks_above_maximum_rejected(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    sub = upload(client, s_token, a["assignment_id"]).get_json()["submission"]
    t_token, _ = teacher_token
    res = client.post(f"/api/submissions/{sub['submission_id']}/grade",
                       json={"marks": 999, "feedback": "too high"}, headers=auth_header(t_token))
    assert res.status_code == 400


def test_unauthorized_grading_rejected(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    sub = upload(client, s_token, a["assignment_id"]).get_json()["submission"]
    res = client.post(f"/api/submissions/{sub['submission_id']}/grade",
                       json={"marks": 50, "feedback": "nice try"}, headers=auth_header(s_token))
    assert res.status_code == 403


def test_student_views_feedback(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    sub = upload(client, s_token, a["assignment_id"]).get_json()["submission"]
    t_token, _ = teacher_token
    client.post(f"/api/submissions/{sub['submission_id']}/grade",
                json={"marks": 70, "feedback": "well done"}, headers=auth_header(t_token))
    res = client.get(f"/api/submissions/{sub['submission_id']}/feedback", headers=auth_header(s_token))
    assert res.status_code == 200
    assert res.get_json()["marks"] == 70


def test_file_download_by_owner(client, teacher_token, student_token):
    a = create_course_and_assignment(client, teacher_token).get_json()["assignment"]
    s_token, _ = student_token
    sub = upload(client, s_token, a["assignment_id"]).get_json()["submission"]
    res = client.get(f"/api/submissions/{sub['submission_id']}/download", headers=auth_header(s_token))
    assert res.status_code == 200
