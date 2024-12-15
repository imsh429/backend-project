from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
jobs_collection = db["jobs"]

class Job:
    @staticmethod
    def find_with_pagination(query, skip, limit, sort_by="created_at", sort_order=-1):
        jobs = list(jobs_collection.find(query).skip(skip).limit(limit).sort(sort_by, sort_order))
        total_count = jobs_collection.count_documents(query)

        # MongoDB `_id` 처리
        for job in jobs:
            job["id"] = str(job["_id"])
            del job["_id"]
        return jobs, total_count
    
    # ID로 공고 조회
    @staticmethod
    def find_by_id(job_id):
        job = jobs_collection.find_one({"_id": ObjectId(job_id)})
        if job:
            job["id"] = str(job["_id"])
            del job["_id"]
        return job

    # 조회수 증가
    @staticmethod
    def increment_views(job_id):
        jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$inc": {"views": 1}})

    # 관련 공고 추천
    @staticmethod
    def find_related(job):
        query = {
            "$or": [
                {"sector": {"$in": job["sector"]}},
                {"tech_stack": {"$in": job["tech_stack"]}}
            ]
        }
        related_jobs = list(jobs_collection.find(query).limit(5))
        for related_job in related_jobs:
            related_job["id"] = str(related_job["_id"])
            del related_job["_id"]
        return related_jobs
