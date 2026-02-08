
# from __future__ import annotations

# import os
# from flask import Flask, jsonify, send_from_directory
# from flask_cors import CORS


# def create_app() -> Flask:
#     app = Flask(__name__)
#     CORS(app)

#     BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#     FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")

#     # -------------------------------
#     # Serve frontend files explicitly
#     # -------------------------------
#     @app.route("/")
#     def index_page():
#         return send_from_directory(FRONTEND_DIR, "index.html")

#     @app.route("/interview")
#     def interview_page():
#         return send_from_directory(FRONTEND_DIR, "interview.html")

#     @app.route("/<path:filename>")
#     def static_files(filename):
#         return send_from_directory(FRONTEND_DIR, filename)

#     # -------------------------------
#     # API
#     # -------------------------------
#     from routes.linkedin import linkedin_bp
#     app.register_blueprint(linkedin_bp)

#     from routes.interview import interview_bp
#     app.register_blueprint(interview_bp, url_prefix="/api/interview")

#     @app.get("/api/health")
#     def health():
#         return jsonify({"ok": True})

#     return app


# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)

from __future__ import annotations
import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

def create_app() -> Flask:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    frontend_dir = os.path.abspath(os.path.join(base_dir, "..", "frontend"))

    # -------------------------------
    # Create Flask app
    # -------------------------------
    app = Flask(
        __name__,
        static_folder=frontend_dir,  # so /js/... and /css/... work
        static_url_path=""
    )
    app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB
    CORS(app)  # Allow cross-origin requests (for localhost:3000 frontend testing)

    # -------------------------------
    # API blueprints
    # -------------------------------
    from routes.linkedin import linkedin_bp
    app.register_blueprint(linkedin_bp, url_prefix="/api/linkedin")

    from routes.interview import interview_bp
    app.register_blueprint(interview_bp)  # blueprint already has /api/interview

    from routes.resume import resume_bp
    app.register_blueprint(resume_bp, url_prefix="/api/resume")

    # -------------------------------
    # Frontend routes
    # -------------------------------
    @app.get("/")
    def index_page():
        return send_from_directory(frontend_dir, "index.html")

    @app.get("/dashboard.html")
    def dashboard_page():
        return send_from_directory(frontend_dir, "dashboard.html")

    @app.get("/linkedin.html")
    def linkedin_page():
        return send_from_directory(frontend_dir, "linkedin.html")

    @app.get("/interview.html")
    def interview_page():
        return send_from_directory(frontend_dir, "interview.html")

    @app.get("/interview")
    def interview_shortcut():
        return send_from_directory(frontend_dir, "interview.html")

    # -------------------------------
    # Health check
    # -------------------------------
    @app.get("/api/health")
    def health():
        return jsonify({"ok": True}), 200

    # -------------------------------
    # Catch-all for static files (JS, CSS, images)
    # -------------------------------
    @app.route("/<path:filename>")
    def static_files(filename):
        return send_from_directory(frontend_dir, filename)

    return app

if __name__ == "__main__":
    app = create_app()
    # Explicitly bind host/port
    app.run(host="127.0.0.1", port=5000, debug=True)
