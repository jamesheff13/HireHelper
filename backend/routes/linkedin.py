# from __future__ import annotations

# import os
# import tempfile
# from typing import Tuple

# from flask import Blueprint, jsonify, request

# from utils.file_parser import parse_pdf


# linkedin_bp = Blueprint("linkedin", __name__, url_prefix="/api/linkedin")

# def _is_allowed_pdf(filename: str) -> bool:
#     return filename.lower().endswith(".pdf")

# @linkedin_bp.post("/upload")
# def upload_linkedin() -> Tuple[object, int]:
#     if "file" not in request.files:
#         return jsonify({"error": "No file part in request."}), 400

#     uploaded = request.files["file"]

#     if not uploaded.filename:
#         return jsonify({"error": "No file selected."}), 400

#     if not _is_allowed_pdf(uploaded.filename):
#         return jsonify({"error": "Only .pdf files are supported for LinkedIn profiles."}), 400

#     tmp_path = None
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             tmp_path = tmp.name
#             uploaded.save(tmp_path)

#         # 🔍 DEBUG CONFIRMATION
#         print("Uploaded LinkedIn PDF:", uploaded.filename)
#         print("Temp path:", tmp_path)
#         print("File size:", os.path.getsize(tmp_path))

#         parsed = parse_pdf(tmp_path)

#         print("Parsed LinkedIn chars:", len(parsed.text))
#         print("First 300 chars:\n", parsed.text[:300])

#         return jsonify(
#             {
#                 "ok": True,
#                 "filename": uploaded.filename,
#                 "linkedin_text": parsed.text,
#                 "page_count": len(parsed.pages),
#             }
#         ), 200

#     except Exception as exc:
#         return jsonify(
#             {"error": "Failed to parse LinkedIn PDF", "details": str(exc)}
#         ), 500

#     finally:
#         if tmp_path and os.path.exists(tmp_path):
#             try:
#                 os.remove(tmp_path)
#             except OSError:
#                 pass

# backend/routes/linkedin.py
from __future__ import annotations

import os
import tempfile
from typing import Tuple

from flask import Blueprint, jsonify, request
from utils.file_parser import parse_pdf
from services.linkedin_service import analyze_linkedin  # <-- added

linkedin_bp = Blueprint("linkedin", __name__, url_prefix="/api/linkedin")

def _is_allowed_pdf(filename: str) -> bool:
    return filename.lower().endswith(".pdf")

@linkedin_bp.post("/upload")
def upload_linkedin() -> Tuple[object, int]:
    if "file" not in request.files:
        return jsonify({"error": "No file part in request."}), 400

    uploaded = request.files["file"]

    if not uploaded.filename:
        return jsonify({"error": "No file selected."}), 400

    if not _is_allowed_pdf(uploaded.filename):
        return jsonify({"error": "Only .pdf files are supported for LinkedIn profiles."}), 400

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp_path = tmp.name
            uploaded.save(tmp_path)

        # 🔍 DEBUG CONFIRMATION
        print("Uploaded LinkedIn PDF:", uploaded.filename)
        print("Temp path:", tmp_path)
        print("File size:", os.path.getsize(tmp_path))

        parsed = parse_pdf(tmp_path)

        print("Parsed LinkedIn chars:", len(parsed.text))
        print("First 300 chars:\n", parsed.text[:300])

        # --- AI ANALYSIS ---
        recommendations = analyze_linkedin(parsed.text)

        return jsonify(
            {
                "ok": True,
                "filename": uploaded.filename,
                "linkedin_text": parsed.text,
                "page_count": len(parsed.pages),
                "recommendations": recommendations,
            }
        ), 200

    except Exception as exc:
        return jsonify(
            {"error": "Failed to parse LinkedIn PDF", "details": str(exc)}
        ), 500

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


