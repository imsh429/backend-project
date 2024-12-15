# 글로벌 에러 핸들러, 커스텀 에러 클래스
from flask import jsonify
from app.utils.logger import logger

# 커스텀 에러 클래스
class CustomError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        if status_code:
            self.status_code = status_code
        self.message = message

    def to_dict(self):
        return {"status": "error", "message": self.message}

class AuthenticationError(CustomError):
    status_code = 401

class ValidationError(CustomError):
    status_code = 400

# 글로벌 에러 핸들러
def register_error_handlers(app):
    @app.errorhandler(CustomError)
    def handle_custom_error(error):
        logger.error(f"Custom Error: {error.message}")
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    @app.errorhandler(500)
    def handle_internal_error(error):
        logger.error(f"Internal Server Error: {str(error)}")
        response = jsonify({"status": "error", "message": "An unexpected error occurred."})
        response.status_code = 500
        return response
