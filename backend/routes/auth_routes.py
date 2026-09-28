"""
routes/auth_routes.py
AUTHENTICATION endpoints: register, login, logout, current-user profile.
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

VALID_ROLES = {"student", "teacher", "admin"}


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or "student").strip().lower()

    # ---- Input validation ----
    if not name or not email or not password:
        return jsonify({"error": "ValidationError", "message": "name, email and password are required."}), 400
    if role not in VALID_ROLES:
        return jsonify({"error": "ValidationError", "message": f"role must be one of {sorted(VALID_ROLES)}"}), 400
    if role == "admin":
        return jsonify({"error": "Forbidden", "message": "Admin accounts cannot be self-registered."}), 403

    required_code = current_app.config["TEACHER_INVITE_CODE"]
    if role == "teacher" and required_code and data.get("invite_code") != required_code:
        return jsonify({"error": "Forbidden", "message": "A valid teacher invite code is required."}), 403
    if len(password) < 6:
        return jsonify({"error": "ValidationError", "message": "password must be at least 6 characters."}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Conflict", "message": "An account with this email already exists."}), 409

    user = User(
        name=name,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registration successful", "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        # Deliberately vague message -- never reveal whether the email exists.
        return jsonify({"error": "Unauthorized", "message": "Invalid email or password."}), 401

    token = create_access_token(
        identity=str(user.user_id),
        additional_claims={"role": user.role, "name": user.name, "email": user.email},
    )
    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "user": user.to_dict(),
    }), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # JWTs are stateless; true logout is client-side token disposal.
    # A production system may add the token's jti to a server-side
    # revocation blocklist (e.g. Redis) for immediate invalidation.
    return jsonify({"message": "Logged out. Please discard the access token client-side."}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "NotFound", "message": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200
