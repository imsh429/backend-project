from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from app.models.review import Review

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

@reviews_bp.route('', methods=['POST'])
@jwt_required()
def add_review():
    """리뷰 추가"""
    user_email = get_jwt_identity()
    data = request.get_json()

    company_id = data.get("company_id")
    rating = data.get("rating")
    review_text = data.get("review_text")

    if not company_id or not rating:
        return jsonify({"status": "error", "message": "Company ID and rating are required."}), 400

    # 동일 회사에 대한 중복 리뷰 확인
    existing_review = Review.find_by_user_and_company(user_email, company_id)
    if existing_review:
        return jsonify({"status": "error", "message": "Review already exists for this company."}), 400

    # 리뷰 추가
    Review.add_review({
        "user_email": user_email,
        "company_id": company_id,
        "rating": rating,
        "review_text": review_text
    })

    return jsonify({"status": "success", "message": "Review added successfully."}), 201

@reviews_bp.route('/<company_id>', methods=['GET'])
@jwt_required()
def get_reviews(company_id):
    """회사 리뷰 조회"""
    reviews = Review.find_by_company(company_id)
    result = []

    for review in reviews:
        result.append({
            "user_email": review["user_email"],
            "rating": review["rating"],
            "review_text": review["review_text"],
            "created_at": review["created_at"]
        })

    return jsonify({"status": "success", "data": result}), 200

@reviews_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    """리뷰 삭제"""
    user_email = get_jwt_identity()
    result = Review.delete_review(review_id, user_email)

    if result.deleted_count == 0:
        return jsonify({"status": "error", "message": "Review not found or unauthorized."}), 404

    return jsonify({"status": "success", "message": "Review deleted successfully."}), 200
