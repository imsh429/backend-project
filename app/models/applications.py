from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId


client = MongoClient("mongodb://113.198.66.75:13115/")
db = client["job_database"]
applications_collection = db["applications"]

class Application:
    @staticmethod
    def create_application(user_email, job_id, cover_letter):
        """새 지원서 생성"""
        application = {
            "user_email": user_email,
            "job_id": job_id,
            "cover_letter": cover_letter,
            "status": "Pending",
            "created_at": datetime.utcnow().isoformat()
        }
        applications_collection.insert_one(application)
        return application

    @staticmethod
    def find_by_user_and_job(user_email, job_id):
        """사용자와 공고 ID로 지원서 조회 (중복 확인)"""
        return applications_collection.find_one({"user_email": user_email, "job_id": job_id})

    @staticmethod
    def find_by_user(user_email):
        """사용자가 제출한 지원 목록 조회"""
        return list(applications_collection.find({"user_email": user_email}))

    @staticmethod
    def find_by_id(application_id):
        """지원서 ID로 지원서 조회"""
        return applications_collection.find_one({"_id": ObjectId(application_id)})

    @staticmethod
    def delete_by_id(application_id):
        """지원서 ID로 지원서 삭제"""
        result = applications_collection.delete_one({"_id": ObjectId(application_id)})
        return result.deleted_count > 0
