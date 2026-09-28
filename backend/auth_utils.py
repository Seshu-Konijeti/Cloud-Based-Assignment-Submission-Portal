"""
auth_utils.py
Authentication (who are you?) and Authorization (what can you do?) helpers.

- Passwords are hashed with werkzeug's PBKDF2 implementation -- never stored
  in plaintext, never logged.
- Identity + role are embedded in a signed JWT (flask_jwt_extended). The
  server trusts nothing from the client except this signed token.
- role_required() is the authorization gate used on every protected route.
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def role_required(*allowed_roles):
    """Decorator: blocks the request unless the JWT's role claim is allowed.
    This is what stops a STUDENT from hitting a TEACHER-only endpoint even
    if they have a valid, unexpired token."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed_roles:
                return jsonify({
                    "error": "Forbidden",
                    "message": f"Role '{role}' is not permitted to perform this action."
                }), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
