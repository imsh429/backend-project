from flask import Blueprint, jsonify, send_file, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

swagger_bp = Blueprint("swagger", __name__, url_prefix="/swagger")

# Swagger UI configuration
SWAGGER_URL = "/swagger"
API_URL = "swagger.yaml"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

@swagger_bp.route('/swagger.yaml', methods=['GET'])
def swagger_spec():
    return send_from_directory(".","swagger.yaml")

# Register Swagger UI blueprint
def init_app(app):
    app.register_blueprint(swaggerui_blueprint)
    app.register_blueprint(swagger_bp)
