#로깅 설정
import logging

# 로깅 설정
def setup_logger():
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.ERROR)  # 에러 레벨 이상의 로그만 기록

    # 파일 핸들러 추가
    file_handler = logging.FileHandler("app_error.log")
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger

# 글로벌 로거 인스턴스
logger = setup_logger()
