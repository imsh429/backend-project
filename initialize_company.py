from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://113.198.66.75:13115/")
db = client["job_database"]

jobs_collection = db["jobs"]
company_collection = db["company"]

def initialize_company_data():
    """jobs 데이터를 기반으로 company 컬렉션 초기화"""
    # Step 1: jobs 컬렉션에 인덱스 생성
    jobs_collection.create_index("company")

    # Step 2: jobs 컬렉션에서 고유한 회사 이름 추출
    unique_companies = jobs_collection.distinct("company")

    # Step 3: company 컬렉션에 데이터 삽입
    for company_name in unique_companies:
        if not company_collection.find_one({"name": company_name}):  # 중복 방지
            # 해당 회사의 공고 데이터 필터링
            company_jobs = list(jobs_collection.find({"company": company_name}))

            # 모든 sector 값을 가져오기
            sectors = [job.get("sector", "Unknown") for job in company_jobs]

            # 공고 개수 계산
            job_count = len(company_jobs)

            # 회사 데이터 삽입
            company_data = {
                "name": company_name,
                "sector": sectors,  # 모든 sector를 리스트로 저장
                "view": 0,
                "job_count": job_count,
                "created_at": datetime.utcnow().isoformat()
            }
            company_collection.insert_one(company_data)

    print("Company 데이터 초기화 완료!")

# 초기화 함수 실행
initialize_company_data()
