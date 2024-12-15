# user 데이터베이스 모델 정의
from pymongo import MongoClient

client = MongoClient("mongodb://seohyeon:123@113.198.66.75:13115/job_database")
db = client["job_database"]
users_collection = db["users"]

# 데이터 조회
users = users_collection.find()
for user in users:
    print(user)

class User:
    def __init__(self, email, password, name, preferred_sector="", preferred_location="", is_admin=""):
        self.email = email
        self.password = password
        self.name = name
        self.preferred_sector = preferred_sector
        self.preferred_location = preferred_location
        self.is_admin = is_admin

    def save(self):
        users_collection.insert_one(self.to_dict())

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "preferred_sector": self.preferred_sector,
            "preferred_location": self.preferred_location,
            "is_admin": self.is_admin
        }

    @staticmethod
    def find_by_email(email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def update_by_email(email, updates):
        return users_collection.update_one({"email": email}, {"$set": updates})
    
    @staticmethod
    def delete_by_email(email):
        return users_collection.delete_one({"email": email})
    
    @staticmethod
    def is_admin(email):
        """사용자의 관리자 여부 확인"""
        user = users_collection.find_one({"email": email})
        return user and user.get("is_admin", False)
    