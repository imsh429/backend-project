#커스텀 에러 클래스
class BaseError(Exception):
    """기본 에러 클래스"""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class AuthenticationError(BaseError):
    """인증 에러"""
    def __init__(self, message="Authentication failed."):
        super().__init__(message, 401)

class ValidationError(BaseError):
    """데이터 유효성 에러"""
    def __init__(self, message="Invalid data format."):
        super().__init__(message, 400)

class NotFoundError(BaseError):
    """리소스 찾기 실패 에러"""
    def __init__(self, message="Resource not found."):
        super().__init__(message, 404)
