"""
Test cases 1-4, 24-25 from the spec's testing strategy:
registration, login (valid/invalid), dashboard authorization, logout.
"""
from conftest import register, login, auth_header


def test_student_registration(client):
    res = register(client, "New Student", "new@example.com", "Password1", "student")
    assert res.status_code == 201
    assert res.get_json()["user"]["role"] == "student"


def test_duplicate_registration_rejected(client):
    register(client, "Dup", "dup@example.com", "Password1", "student")
    res = register(client, "Dup2", "dup@example.com", "Password1", "student")
    assert res.status_code == 409


def test_teacher_login_valid(client, teacher_token):
    token, user = teacher_token
    assert token is not None
    assert user["role"] == "teacher"


def test_login_invalid_password(client):
    register(client, "X", "x@example.com", "CorrectPass1", "student")
    res = client.post("/api/login", json={"email": "x@example.com", "password": "WrongPass"})
    assert res.status_code == 401


def test_student_cannot_access_teacher_dashboard(client, student_token):
    token, _ = student_token
    res = client.get("/api/dashboard/teacher", headers=auth_header(token))
    assert res.status_code == 403


def test_teacher_cannot_access_student_dashboard(client, teacher_token):
    token, _ = teacher_token
    res = client.get("/api/dashboard/student", headers=auth_header(token))
    assert res.status_code == 403


def test_protected_route_requires_token(client):
    res = client.get("/api/dashboard/student")
    assert res.status_code == 401


def test_logout(client, student_token):
    token, _ = student_token
    res = client.post("/api/logout", headers=auth_header(token))
    assert res.status_code == 200

def test_teacher_registration_requires_invite_code(app, client):
    app.config["TEACHER_INVITE_CODE"] = "SECRET123"
    res = client.post("/api/register", json={
        "name": "Fake Teacher", "email": "fake@example.com",
        "password": "Password1", "role": "teacher"
    })
    assert res.status_code == 403

    res = client.post("/api/register", json={
        "name": "Real Teacher", "email": "real@example.com",
        "password": "Password1", "role": "teacher", "invite_code": "SECRET123"
    })
    assert res.status_code == 201


def test_admin_cannot_self_register(client):
    res = client.post("/api/register", json={
        "name": "Hacker", "email": "hack@example.com",
        "password": "Password1", "role": "admin"
    })
    assert res.status_code == 403
