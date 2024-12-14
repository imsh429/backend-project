from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.feedback import Feedback

feedback_bp = Blueprint("feedback", __name__, url_prefix="/feedback")

@feedback_bp.route('', methods=['POST'])
@jwt_required()
def submit_feedback():
    """피드백 제출"""
    user_email = get_jwt_identity()
    data = request.get_json()

    feedback_type = data.get("feedback_type")
    message = data.get("message")

    if not feedback_type or not message:
        return jsonify({"status": "error", "message": "Feedback type and message are required."}), 400

    feedback = Feedback.create_feedback(user_email, feedback_type, message)
    return jsonify({"status": "success", "data": feedback}), 201

@feedback_bp.route('', methods=['GET'])
@jwt_required()
def get_feedback():
    """피드백 목록 조회"""
    filters = {}
    feedback_type = request.args.get("feedback_type")
    user_email = request.args.get("user_email")

    if feedback_type:
        filters["feedback_type"] = feedback_type
    if user_email:
        filters["user_email"] = user_email

    feedbacks = Feedback.get_feedbacks(filters)
    return jsonify({"status": "success", "data": feedbacks}), 200
