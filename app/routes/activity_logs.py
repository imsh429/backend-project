from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.activity_log import ActivityLog
from app.utils.error_handler import ValidationError

activity_logs_bp = Blueprint("activity_logs", __name__, url_prefix="/activity-logs")

# 활동 로그 조회
@activity_logs_bp.route('', methods=['GET'])
@jwt_required()
def get_activity_logs():
    """활동 로그 조회"""
    user_email = get_jwt_identity()
    try:
        page = request.args.get("page", 1, type=int)
        if page < 1:
            raise ValidationError("Page number must be 1 or greater.")
    except ValueError:
        raise ValidationError("Page number must be an integer.")
    per_page = 10  # 페이지당 항목 수

    try:
        # 로그 조회
        logs, total_items, total_pages = ActivityLog.get_logs(user_email, page, per_page)
    except Exception as e:
        raise ValidationError(f"Failed to fetch activity logs: {str(e)}")

    return jsonify({
        "status": "success",
        "data": logs,
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        }
    }), 200
