import pandas as pd
from pymongo import MongoClient
import re

# MongoDB 연결 설정
def connect_to_mongo():
    client = MongoClient("mongodb://113.198.66.75:13115/")  # MongoDB 서버 정보
    db = client["job_database"]  # 데이터베이스 이름
    return db

# 컬렉션별 데이터 저장
def save_to_collections(db, csv_file):
    # CSV 데이터 읽기
    df = pd.read_csv(csv_file)

    # 1. jobs 컬렉션
    jobs_collection = db["jobs"]
    for _, row in df.iterrows():

        # `created_at`을 ISO 8601 날짜 형식으로 변환
        created_at = re.sub(r'(수정일|등록일)\s', '', row['created_at']).strip()
        created_at = pd.to_datetime(created_at, format='%y/%m/%d').isoformat()

        # `salary`를 숫자로 변환
        if pd.notna(row['salary']):  # NaN 값 체크
            try:
                # 쉼표와 '만원' 제거 후 숫자로 변환
                salary = int(str(row['salary']).replace(',', '').replace('만원', '').strip())
            except ValueError:
                salary = None  # 변환 실패 시 None 설정
        else:
            salary = None

        # `sector`와 `tech_stack`을 배열로 변환
        sector = eval(row['sector']) if isinstance(row['sector'], str) else []
        tech_stack = eval(row['tech_stack']) if isinstance(row['tech_stack'], str) else []

        if not jobs_collection.find_one({"link": row['link']}):  # 중복 방지
            jobs_collection.insert_one({
                "company": row['company'],
                "title": row['title'],
                "link": row['link'],
                "location": row['location'],
                "experience": row['experience'],
                "education": row['education'],
                "employment_type": row['employment_type'],
                "deadline": row['deadline'],
                "sector": sector,
                "salary": salary,
                'created_at': created_at,
                'views': row['views'],
                'tech_stack': tech_stack   
            })


    print("데이터 저장 완료")

if __name__ == "__main__":
    # MongoDB 연결
    db = connect_to_mongo()

    # CSV 파일 경로
    csv_file = "saramin_python.csv"  # 크롤링 코드에서 생성된 CSV 파일

    # 데이터 저장
    save_to_collections(db, csv_file)
