from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.activity_log import ActivityLog

activity_logs_bp = Blueprint("activity_logs", __name__, url_prefix="/activity-logs")

# 활동 로그 조회
@activity_logs_bp.route('', methods=['GET'])
@jwt_required()
def get_activity_logs():
    """활동 로그 조회"""
    user_email = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = 10  # 페이지당 항목 수

    logs, total_items, total_pages = ActivityLog.get_logs(user_email, page, per_page)

    return jsonify({
        "status": "success",
        "data": logs,
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        }
    }), 200
