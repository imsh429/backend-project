# 회원관리 api 구현 
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.models.activity_log import ActivityLog
from app.utils.jwt_handler import generate_tokens
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta
import re
import base64

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# 회원가입 API
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # 데이터 검증
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    preferred_sector = data.get('preferred_sector', "")
    preferred_location = data.get('preferred_location', "")
    is_admin = data.get('is_admin', False)  # 관리자 여부 (기본값: False)

    if not email or not password or not name:
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    # 이메일 형식 검증
    email_regex = r'^\S+@\S+\.\S+$'
    if not re.match(email_regex, email):
        return jsonify({"status": "error", "message": "Invalid email format."}), 400

    # 이메일 중복 확인
    if User.find_by_email(email):
        return jsonify({"status": "error", "message": "Email already exists."}), 400

    # 비밀번호 암호화 (Base64)
    encrypted_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    # 사용자 데이터 저장
    user = User(email=email, password=encrypted_password, name=name,
                preferred_sector=preferred_sector, preferred_location=preferred_location, is_admin= is_admin)
    user.save()

    return jsonify({"status": "success", "message": "User registered successfully."}), 201

# 로그인 API
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # 데이터 검증
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing email or password."}), 400

    # 사용자 확인
    user = User.find_by_email(email)
    if not user:
        return jsonify({"status": "error", "message": "Invalid credentials."}), 401

    # 비밀번호 검증
    encrypted_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    if user['password'] != encrypted_password:
        return jsonify({"status": "error", "message": "Invalid credentials."}), 401

    # JWT 토큰 발급
    tokens = generate_tokens(email)

    # activity_log에 기록
    ActivityLog.log(email, "login", "User logged in successfully")

    return jsonify({"status": "success", "token": tokens}), 200

# jwt 토큰 갱신
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Refresh 토큰 인증 필요
def refresh():
    # 현재 사용자 식별 정보
    identity = get_jwt_identity()
    
    # 새로운 Access 토큰 생성
    new_access_token = create_access_token(identity=identity, expires_delta=timedelta(days=1))
    
    return jsonify({"status": "success", "token": new_access_token}), 200

# 회원정보 수정
@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()  # JWT 인증 필요
def update_profile():
    identity = get_jwt_identity()  # 현재 사용자 이메일
    data = request.get_json()

    # 수정 가능한 필드
    updates = {}
    if "name" in data and data["name"]:
        updates["name"] = data["name"]
    if "password" in data and data["password"]:
        updates["password"] = base64.b64encode(data["password"].encode('utf-8')).decode('utf-8')
    if "preferred_sector" in data and data["preferred_sector"]:
        updates["preferred_sector"] = data["preferred_sector"]
    if "preferred_location" in data and data["preferred_location"]:
        updates["preferred_location"] = data["preferred_location"]

    # 수정할 데이터가 없으면 에러 반환
    if not updates:
        return jsonify({"status": "error", "message": "No data to update."}), 400

    # 사용자 데이터 업데이트
    result = User.update_by_email(identity, updates)
    if result.modified_count == 0:
        return jsonify({"status": "error", "message": "Failed to update profile."}), 500

    return jsonify({"status": "success", "message": "Profile updated successfully."}), 200

# 사용자 데이터 삭제 API
@auth_bp.route('/profile', methods=['DELETE'])
@jwt_required()  # JWT 인증 필요
def delete_profile():
    identity = get_jwt_identity()  # 현재 사용자 이메일

    # 사용자 데이터 삭제
    result = User.delete_by_email(identity)
    if result.deleted_count == 0:
        return jsonify({"status": "error", "message": "Failed to delete account."}), 500

    return jsonify({
        "status": "success",
        "message": "Account deleted successfully"
    }), 200


# 사용자 정보 조회 API
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()  # JWT 인증 필요
def get_profile():
    identity = get_jwt_identity()  # 현재 사용자 이메일

    # 사용자 데이터 조회
    user = User.find_by_email(identity)
    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    # 비밀번호를 제외한 데이터 반환
    user_data = {
        "email": user["email"],
        "name": user.get("name", ""),
        "preferred_sector": user.get("preferred_sector", ""),
        "preferred_location": user.get("preferred_location", "")
    }

    return jsonify({"status": "success", "data": user_data}), 200