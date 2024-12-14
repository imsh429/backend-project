from datetime import datetime
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify
from app.models.jobs import Job, jobs_collection
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.user import User

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('', methods=['GET'])
@jwt_required()  # JWT 인증 필요
def get_jobs():
    # 쿼리 파라미터
    page = int(request.args.get('page', 1))
    location = request.args.get('location')
    experience = request.args.get('experience')
    salary = request.args.get('salary')
    tech_stack = request.args.get('tech_stack')
    keyword = request.args.get('keyword')
    sort_by = request.args.get('sort_by', 'created_at')  # 기본 정렬: 등록일
    order = request.args.get('order', 'desc')  # 기본 정렬 순서: 내림차순


    # 페이지 크기와 스킵 계산
    page_size = 20
    skip = (page - 1) * page_size

    # 필터링 조건
    query = {}
    if location:
        query["location"] = {"$regex": location, "$options": "i"}
    if experience:
        query["experience"] = {"$regex": experience, "$options": "i"}
    if salary:
        try:
            query["salary"] = {"$gte": int(salary)}
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid salary value"}), 400
    if tech_stack:
        query["tech_stack"] = {"$in": tech_stack}
    if keyword:
        query["$or"] = [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"company": {"$regex": keyword, "$options": "i"}},
            {"sector": {"$regex": keyword, "$options": "i"}}
        ]

    # 정렬 처리
    valid_sort_fields = ["created_at", "deadline"]
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"
    sort_order = -1 if order == "desc" else 1

    # 데이터베이스 조회
    jobs, total_count = Job.find_with_pagination(query, skip, page_size, sort_by, sort_order)
    total_pages = (total_count + page_size - 1) // page_size

    response = {
        "status": "success",
        "data": jobs,
        "pagination": {
            "currentPage": page,
            "totalPages": total_pages,
            "totalItems": total_count
        }
    }

    return jsonify(response), 200

# 공고 상세 조회
@jobs_bp.route('/<job_id>', methods=['GET'])
def get_job_details(job_id):
    # 공고 조회
    job = Job.find_by_id(job_id)
    if not job:
        return jsonify({"status": "error", "message": "Job not found."}), 404

    # 조회수 증가
    Job.increment_views(job_id)

    # 관련 공고 추천
    related_jobs = Job.find_related(job)

    # 응답 생성
    response = {
        "status": "success",
        "data": job,
        "related_jobs": related_jobs
    }
    return jsonify(response), 200

@jobs_bp.route('', methods=['POST'])
@jwt_required()  # JWT 인증 필요
def create_job():
    identity = get_jwt_identity()

    # 관리자 권한 확인
    if not User.is_admin(identity):
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    # 요청 데이터 가져오기
    data = request.get_json()
    required_fields = ["title", "company", "location", "sector", "description", "deadline"]
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    # 새 공고 데이터 저장
    job = {
        "title": data["title"],
        "company": data["company"],
        "location": data["location"],
        "sector": data["sector"],
        "experience": data.get("experience"),
        "salary": data.get("salary"),
        "tech_stack": data.get("tech_stack", []),
        "description": data["description"],
        "deadline": data["deadline"],
        "created_at": datetime.utcnow().isoformat(),
        "views": 0
    }
    jobs_collection.insert_one(job)

    return jsonify({"status": "success", "message": "Job posting created successfully."}), 201

@jobs_bp.route('/<job_id>', methods=['PUT'])
@jwt_required()  # JWT 인증 필요
def update_job(job_id):
    identity = get_jwt_identity()

    # 관리자 권한 확인
    if not User.is_admin(identity):
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    # 요청 데이터 가져오기
    updates = request.get_json()
    if not updates:
        return jsonify({"status": "error", "message": "No data to update."}), 400

    # 공고 수정
    try:
        result = jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$set": updates})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    if result.matched_count == 0:
        return jsonify({"status": "error", "message": "Job not found."}), 404

    return jsonify({"status": "success", "message": "Job posting updated successfully."}), 200

@jobs_bp.route('/<job_id>', methods=['DELETE'])
@jwt_required()  # JWT 인증 필요
def delete_job(job_id):
    identity = get_jwt_identity()

    # 관리자 권한 확인
    if not User.is_admin(identity):
        return jsonify({"status": "error", "message": "Unauthorized."}), 403

    # 공고 삭제
    try:
        result = jobs_collection.delete_one({"_id": ObjectId(job_id)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

    if result.deleted_count == 0:
        return jsonify({"status": "error", "message": "Job not found."}), 404

    return jsonify({"status": "success", "message": "Job posting deleted successfully."}), 200