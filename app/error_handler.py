from flask import jsonify
from app.models.errors import BaseError
from app.utils.logger import log_error

def register_error_handlers(app):
    """글로벌 에러 핸들러 등록"""

    @app.errorhandler(BaseError)
    def handle_custom_error(error):
        """커스텀 에러 처리"""
        response = jsonify({
            "status": "error",
            "message": error.message
        })
        response.status_code = error.status_code
        log_error(f"{error.status_code} - {error.message}")
        return response

    @app.errorhandler(Exception)
    def handle_general_error(error):
        """예상치 못한 에러 처리"""
        response = jsonify({
            "status": "error",
            "message": "An unexpected error occurred."
        })
        response.status_code = 500
        log_error(f"500 - {str(error)}")
        return response
