from flask import Flask
from flask_jwt_extended import JWTManager
from app.routes.auth import auth_bp
from app.routes.jobs import jobs_bp  # 채용 공고 라우트 추가
from app.routes.applications import applications_bp
from app.routes.bookmarks import bookmarks_bp
from app.routes.activity_logs import activity_logs_bp
from app.routes.company import company_bp
from app.routes.reviews import reviews_bp
from app.routes.swagger import init_app as init_swagger  # Swagger 관련 초기화
from flask_cors import CORS
from app.routes.feedback import feedback_bp

def create_app():
    app = Flask(__name__)

    # JWT 설정
    app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"  # JWT를 위한 비밀키

    init_swagger(app)


    # JWT 매니저 초기화
    jwt = JWTManager(app)

    CORS(app)
    

    # 블루프린트 등록
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)  # 채용 공고 라우트 등록
    app.register_blueprint(applications_bp)
    app.register_blueprint(bookmarks_bp)
    app.register_blueprint(activity_logs_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(feedback_bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=80, debug=True)
