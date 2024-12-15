# Flask 애플리케이션 초기화
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta  # datetime에서 timedelta를 가져옵니다.
from app.routes.jobs import jobs_bp
from app.error_handler import register_error_handlers
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(jobs_bp)  # jobs 라우트 등록
    CORS(app, resources={r"/*": {"origins": "*"}})

    # JWT 설정
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    JWTManager(app)
    #에러핸들러 ㄷ등록
    register_error_handlers(app)


    return app
