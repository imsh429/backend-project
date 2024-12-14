# Flask 애플리케이션 초기화
from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta  # datetime에서 timedelta를 가져옵니다.
from app.routes.jobs import jobs_bp
from app.routes.swagger import init_app as init_swagger

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(jobs_bp)  # jobs 라우트 등록


    # JWT 설정
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=3)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    app = Flask(__name__)
    init_swagger(app)
    
    JWTManager(app)

    return app
