from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
feedback_collection = db["feedback"]

class Feedback:
    @staticmethod
    def create_feedback(user_email, feedback_type, message):
        """새 피드백 생성"""
        feedback = {
            "user_email": user_email,
            "feedback_type": feedback_type,
            "message": message,
            "created_at": datetime.utcnow().isoformat()
        }
        feedback_collection.insert_one(feedback)
        feedback["_id"] = str(feedback["_id"])  # ObjectId를 문자열로 변환
        return feedback

    @staticmethod
    def get_feedbacks(filters=None):
        """피드백 조회"""
        query = filters or {}
        feedbacks = feedback_collection.find(query)

        return [{**fb, "_id": str(fb["_id"])} for fb in feedbacks]

    @staticmethod
    def get_feedback_by_id(feedback_id):
        """특정 피드백 ID로 조회"""
        feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
        if feedback:
            feedback["_id"] = str(feedback["_id"])  # ObjectId를 문자열로 변환
        return feedback