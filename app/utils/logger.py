import logging

# 로그 설정
logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # 파일에 로그 저장
        logging.StreamHandler()         # 콘솔 출력
    ]
)

def log_error(message):
    """에러 로그 기록"""
    logging.error(message)
