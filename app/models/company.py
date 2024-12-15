from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
company_collection = db["company"]

class Company:
    @staticmethod
    def create_index():
        """인덱스 생성"""
        company_collection.create_index("name", unique=True)

    @staticmethod
    def find_all(page, per_page):
        """모든 회사 목록 반환 (페이지네이션 포함)"""
        skip = (page - 1) * per_page
        companies = company_collection.find().sort("created_at", -1).skip(skip).limit(per_page)
        total_items = company_collection.count_documents({})
        total_pages = (total_items + per_page - 1) // per_page
        return list(companies), total_items, total_pages

    @staticmethod
    def find_by_id(company_id):
        """ID로 회사 조회"""
        return company_collection.find_one({"_id": ObjectId(company_id)})

    @staticmethod
    def increment_view(company_id):
        """조회수 증가"""
        company_collection.update_one({"_id": ObjectId(company_id)}, {"$inc": {"view": 1}})

    @staticmethod
    def insert(data):
        """새로운 회사 추가"""
        data["created_at"] = datetime.utcnow().isoformat()
        company_collection.insert_one(data)
