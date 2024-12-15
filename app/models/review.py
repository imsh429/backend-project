from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
reviews_collection = db["reviews"]

class Review:
    @staticmethod
    def find_by_company(company_id):
        """특정 회사의 리뷰 조회"""
        return list(reviews_collection.find({"company_id": company_id}))

    @staticmethod
    def find_by_user_and_company(user_email, company_id):
        """특정 사용자와 회사의 리뷰 조회"""
        return reviews_collection.find_one({"user_email": user_email, "company_id": company_id})

    @staticmethod
    def add_review(data):
        """리뷰 추가"""
        data["created_at"] = datetime.utcnow().isoformat()
        reviews_collection.insert_one(data)

    @staticmethod
    def delete_review(review_id, user_email):
        """리뷰 삭제"""
        return reviews_collection.delete_one({"_id": ObjectId(review_id), "user_email": user_email})
