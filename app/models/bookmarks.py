from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
bookmarks_collection = db["bookmarks"]

class Bookmark:
    @staticmethod
    def find_by_user_and_job(user_email, job_id):
        """특정 사용자와 공고 ID로 북마크 조회"""
        return bookmarks_collection.find_one({"user_email": user_email, "job_id": job_id})

    @staticmethod
    def add_bookmark(user_email, job_id):
        """북마크 추가"""
        new_bookmark = {
            "user_email": user_email,
            "job_id": job_id,
            "created_at": datetime.utcnow().isoformat()
        }
        bookmarks_collection.insert_one(new_bookmark)

    @staticmethod
    def remove_bookmark(bookmark_id):
        """북마크 삭제"""
        bookmarks_collection.delete_one({"_id": ObjectId(bookmark_id)})
