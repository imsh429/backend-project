# jwt 토큰 처리 (발급 빛 검증)
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta

def generate_tokens(email):
    access_token = create_access_token(identity=email, expires_delta=timedelta(days=1))
    refresh_token = create_refresh_token(identity=email, expires_delta=timedelta(days=7))
    return {"access": access_token, "refresh": refresh_token}