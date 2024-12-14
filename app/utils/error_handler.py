from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)

# 커스텀 에러 클래스
class AuthenticationError(Exception):
    """인증 관련 에러"""
    def __init__(self, message="Authentication failed."):
        self.message = message
        self.status_code = 401

class ValidationError(Exception):
    """데이터 유효성 에러"""
    def __init__(self, message="Invalid request data."):
        self.message = message
        self.status_code = 400

# 글로벌 에러 핸들러
def register_error_handlers(app):
    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(e):
        logging.error(f"AuthenticationError: {e.message}")
        return jsonify({"status": "error", "message": e.message}), e.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        logging.error(f"ValidationError: {e.message}")
        return jsonify({"status": "error", "message": e.message}), e.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        logging.error(f"HTTPException: {e.description}")
        return jsonify({"status": "error", "message": e.description}), e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e):
        logging.error(f"UnhandledException: {str(e)}")
        return jsonify({"status": "error", "message": "An unexpected error occurred."}), 500
