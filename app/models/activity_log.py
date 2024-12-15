from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
activity_logs_collection = db["activity_logs"]

class ActivityLog:
    @staticmethod
    def log(user_email, action, details=""):
        """사용자 활동 로그 기록"""
        activity_log = {
            "user_email": user_email,
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        activity_logs_collection.insert_one(activity_log)

    @staticmethod
    def get_logs(user_email, page, per_page):
        """사용자 활동 로그 조회"""
        query = {"user_email": user_email}
        total_items = activity_logs_collection.count_documents(query)
        total_pages = (total_items + per_page - 1) // per_page  # 전체 페이지 계산

        logs = activity_logs_collection.find(query).sort("timestamp", -1).skip((page - 1) * per_page).limit(per_page)

        result = []
        for log in logs:
            result.append({
                "action": log["action"],
                "details": log["details"],
                "timestamp": log["timestamp"]
            })

        return result, total_items, total_pages
