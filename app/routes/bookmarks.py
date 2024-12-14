from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.bookmarks import Bookmark
from app.models.jobs import jobs_collection
from app.models.bookmarks import bookmarks_collection
from app.models.activity_log import ActivityLog

bookmarks_bp = Blueprint("bookmarks", __name__, url_prefix="/bookmarks")

@bookmarks_bp.route('', methods=['POST'])
@jwt_required()
def toggle_bookmark():
    """북마크 추가/제거"""
    user_email = get_jwt_identity()
    data = request.get_json()
    job_id = data.get("job_id")

    if not job_id:
        return jsonify({"status": "error", "message": "Job ID is required."}), 400
    
    # 유효한 공고인지 확인
    job = jobs_collection.find_one({"_id": ObjectId(job_id)})
    if not job:
        return jsonify({"status": "error", "message": "Invalid Job ID."}), 400

    # 북마크 존재 여부 확인
    existing_bookmark = Bookmark.find_by_user_and_job(user_email, job_id)

    if existing_bookmark:
        # 북마크 제거
        Bookmark.remove_bookmark(existing_bookmark["_id"])
        return jsonify({"status": "success", "message": "Bookmark removed successfully."}), 200
    else:
        # 북마크 추가
        Bookmark.add_bookmark(user_email, job_id)
        # activity_log에 기록
        ActivityLog.log(user_email, "add_Bookmarks", f"bookmarked job: {job_id}")
        return jsonify({"status": "success", "message": "Bookmark added successfully."}), 201
    
@bookmarks_bp.route('', methods=['GET'])
@jwt_required()
def get_bookmarks():
    """북마크 목록 조회"""
    user_email = get_jwt_identity()

    # 쿼리 파라미터 처리
    page = request.args.get("page", 1, type=int)
    per_page = 10  # 페이지당 항목 수

    # 사용자별 북마크 조회
    query = {"user_email": user_email}
    total_items = bookmarks_collection.count_documents(query)
    total_pages = (total_items + per_page - 1) // per_page  # 전체 페이지 계산

    # 페이지네이션 및 정렬
    bookmarks = bookmarks_collection.find(query).sort("created_at", -1).skip((page - 1) * per_page).limit(per_page)

    # 결과 변환
    result = []
    for bookmark in bookmarks:
        result.append({
            "job_id": bookmark["job_id"],
            "created_at": bookmark["created_at"]
        })

    return jsonify({
        "status": "success",
        "data": result,
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_items
        }
    }), 200

