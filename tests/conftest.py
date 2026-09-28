"""
tests/conftest.py
Shared pytest fixtures: an isolated in-memory app + helpers to
register/login users and create assignments quickly in tests.
"""
import io
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app import create_app
from config import Config
from database import db


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    JWT_SECRET_KEY = "test-secret"
    SECRET_KEY = "test-secret"
    LOCAL_STORAGE_ROOT = "/tmp/cloud_portal_test_storage"
    TEACHER_INVITE_CODE = ""   # disable the invite check for automated tests


@pytest.fixture()
def app():
    application = create_app(TestConfig)
    yield application
    with application.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, name, email, password, role):
    return client.post("/api/register", json={
        "name": name, "email": email, "password": password, "role": role
    })


def login(client, email, password):
    res = client.post("/api/login", json={"email": email, "password": password})
    return res.get_json()["access_token"], res.get_json()["user"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def teacher_token(client):
    register(client, "Teacher One", "t1@example.com", "Teacher@123", "teacher")
    token, user = login(client, "t1@example.com", "Teacher@123")
    return token, user


@pytest.fixture()
def student_token(client):
    register(client, "Student One", "s1@example.com", "Student@123", "student")
    token, user = login(client, "s1@example.com", "Student@123")
    return token, user


@pytest.fixture()
def another_student_token(client):
    register(client, "Student Two", "s2@example.com", "Student@123", "student")
    token, user = login(client, "s2@example.com", "Student@123")
    return token, user
