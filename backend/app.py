"""
app.py
Application factory + entrypoint.

Run locally:
    python app.py

This wires together:
  - Flask app + config (from environment variables, see .env.example)
  - SQLAlchemy (cloud database stand-in)
  - JWT auth (cloud authentication stand-in)
  - CORS (so the static/React frontend on a different port/host can call the API)
  - Blueprints for every REST resource
  - Global error handlers (consistent JSON error shape + status codes)
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database import db

from routes.auth_routes import auth_bp
from routes.course_routes import course_bp
from routes.assignment_routes import assignment_bp
from routes.submission_routes import submission_bp
from routes.dashboard_routes import dashboard_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    JWTManager(app)
    CORS(app, origins=app.config["CORS_ORIGINS"])

    app.register_blueprint(auth_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(assignment_bp)
    app.register_blueprint(submission_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "service": "cloud-assignment-portal-backend"}), 200

    # ---- Global error handlers: consistent JSON responses ----
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "NotFound", "message": "Resource not found."}), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify({"error": "PayloadTooLarge", "message": "Uploaded file exceeds the maximum allowed size."}), 413

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "InternalServerError", "message": "Something went wrong. Please try again."}), 500

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
