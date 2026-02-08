from __future__ import annotations
from services.ai_service import analyze_resume


import os
import tempfile
from typing import Tuple

from flask import Blueprint, jsonify, request

from utils.file_parser import parse_docx
from services.resume_service import set_resume, get_resume


resume_bp = Blueprint("resume", __name__, url_prefix="/api/resume")


def _is_allowed_docx(filename: str) -> bool:
    # Minimal check. Real validation is reading the file successfully.
    return filename.lower().endswith(".docx")


@resume_bp.post("/upload")
def upload_resume() -> Tuple[object, int]:
    """
    Accepts a resume Word file (.docx) as multipart/form-data.

    Frontend should send:
      - form field name: "file"
      - content: .docx
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part in request. Use form field name 'file'."}), 400

    uploaded = request.files["file"]

    if not uploaded.filename:
        return jsonify({"error": "No file selected."}), 400

    if not _is_allowed_docx(uploaded.filename):
        return jsonify({"error": "Only .docx files are supported for resumes."}), 400

    # Save to a temp file so python-docx can read it
    tmp_path = None
    try:
        suffix = ".docx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp_path = tmp.name
            uploaded.save(tmp_path)
        
        #test
        print("Uploaded filename:", uploaded.filename)
        print("Saved temp path:", tmp_path)
        print("Temp file size:", os.path.getsize(tmp_path))

        parsed = parse_docx(tmp_path)
        
        #test
        print("Parsed resume chars:", len(parsed.text))
        print("First 300 chars:\n", parsed.text[:300])

        return jsonify(
            {
                "ok": True,
                "filename": uploaded.filename,
                "resume_text": parsed.text,
                "paragraph_count": len(parsed.paragraphs),
            }
        ), 200

    except Exception as exc:
        # Keep error messages simple for now
        return jsonify({"error": "Failed to parse resume .docx", "details": str(exc)}), 500

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass

    





@resume_bp.post("/analyze")
def analyze_resume_route() -> Tuple[object, int]:
    data = request.get_json(silent=True) or {}
    resume_text = (data.get("resume_text") or "").strip()

    if not resume_text:
        return jsonify({"error": "No resume_text provided."}), 400

    result = analyze_resume(resume_text)
    return jsonify(result), 200
