#mock interview

from flask import Blueprint, request, jsonify
from services.interview_service import InterviewService

interview_bp = Blueprint("interview", __name__, url_prefix="/api/interview")

# Store a single interview session for now
service = InterviewService()

@interview_bp.route("/start", methods=["POST"])
def start_interview():
    data = request.get_json()
    role = data.get("role", "Software Engineer")
    service.start(role)
    question = service.current_question
    return jsonify({"question": question})

@interview_bp.route("/answer", methods=["POST"])
def answer_question():
    data = request.get_json()
    answer = data.get("answer", "")
    next_question = service.next(answer)
    return jsonify({"question": next_question})

@interview_bp.route("/finish", methods=["POST"])
def finish_interview():
    feedback = service.finish()
    return jsonify({"feedback": feedback})
