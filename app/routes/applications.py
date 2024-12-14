from bson import ObjectId
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.applications import Application, applications_collection
from app.models.jobs import jobs_collection
from app.models.activity_log import ActivityLog

applications_bp = Blueprint("applications", __name__, url_prefix="/applications")

# 지원하기 API
@applications_bp.route('', methods=['POST'])
@jwt_required()
def apply_for_job():
    user_email = get_jwt_identity()
    data = request.get_json()

    job_id = data.get("job_id")
    cover_letter = data.get("cover_letter", "")

    if not job_id:
        return jsonify({"status": "error", "message": "Job ID is required."}), 400
    
    # 유효한 공고인지 확인
    job = jobs_collection.find_one({"_id": ObjectId(job_id)})
    if not job:
        return jsonify({"status": "error", "message": "Invalid Job ID."}), 400

    # 중복 지원 체크
    if Application.find_by_user_and_job(user_email, job_id):
        return jsonify({"status": "error", "message": "You have already applied for this job."}), 400
    
    # activity_log에 기록
    ActivityLog.log(user_email, "applied_for_job", f"Applied for job: {job_id}")


    # 지원 정보 저장
    application = Application.create_application(user_email, job_id, cover_letter)
    return jsonify({"status": "success", "message": "Application submitted successfully."}), 201


# 지원 내역 조회 API
@applications_bp.route('', methods=['GET'])
@jwt_required()
def get_applications():
    """지원 내역 조회"""
    user_email = get_jwt_identity()

    # 쿼리 파라미터 처리
    status = request.args.get("status")  # 상태 필터링
    sort_by = request.args.get("sort_by", "created_at")  # 정렬 기준 (기본값: created_at)
    page = int(request.args.get("page", 1))  # 페이지 번호 (기본값: 1)
    page_size = 20  # 페이지 크기

    # 기본 쿼리
    query = {"user_email": user_email}
    if status:
        query["status"] = status

    # 페이지네이션을 적용한 데이터 조회
    total_count = applications_collection.count_documents(query)
    applications = applications_collection.find(query).sort(
        sort_by, -1  # 최신순 정렬
    ).skip((page - 1) * page_size).limit(page_size)

    # 결과 변환
    result = []
    for app in applications:
        app["id"] = str(app["_id"])
        del app["_id"]
        result.append(app)

    # 응답 생성
    response = {
        "status": "success",
        "data": result,
        "pagination": {
            "currentPage": page,
            "totalPages": (total_count + page_size - 1) // page_size,  # 총 페이지 수
            "totalItems": total_count  # 총 지원 개수
        }
    }
    return jsonify(response), 200

# 지원 취소 API
@applications_bp.route('/<application_id>', methods=['DELETE'])
@jwt_required()
def cancel_application(application_id):
    """지원 취소"""
    user_email = get_jwt_identity()

    # 지원서 조회
    application = applications_collection.find_one({"_id": ObjectId(application_id), "user_email": user_email})
    if not application:
        return jsonify({"status": "error", "message": "Application not found."}), 404

    # 지원서 삭제
    result = applications_collection.delete_one({"_id": ObjectId(application_id)})
    if result.deleted_count == 0:
        return jsonify({"status": "error", "message": "Failed to cancel application."}), 500

    return jsonify({"status": "success", "message": "Application deleted successfully."}), 200
