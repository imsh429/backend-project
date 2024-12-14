from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app.models.company import Company

company_bp = Blueprint("company", __name__, url_prefix="/company")

@company_bp.route('', methods=['GET'])
@jwt_required()
def get_company_list():
    """회사 목록 조회"""
    user_email = get_jwt_identity()

    # 쿼리 파라미터 처리
    page = request.args.get("page", 1, type=int)
    per_page = 20

    # 회사 목록 및 페이지네이션 정보 가져오기
    companies, total_items, total_pages = Company.find_all(page, per_page)

    # 결과 변환
    result = []
    for company in companies:
        result.append({
            "id": str(company["_id"]),
            "name": company["name"],
            "sector": company["sector"],
            "view": company["view"],
            "job_count": company["job_count"]
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

@company_bp.route('/<company_id>', methods=['GET'])
@jwt_required()
def get_company(company_id):
    """회사 정보 조회"""
    company = Company.find_by_id(company_id)
    if not company:
        return jsonify({"status": "error", "message": "Company not found."}), 404

    # 조회수 증가
    Company.increment_view(company_id)

    # 결과 반환
    company["id"] = str(company["_id"])
    del company["_id"]
    return jsonify({"status": "success", "data": company}), 200
