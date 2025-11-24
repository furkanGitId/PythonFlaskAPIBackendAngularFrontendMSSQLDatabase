from flask import Flask
from flasgger import Flasgger
import importlib
try:
    jwt_ext = importlib.import_module('flask_jwt_extended')
    JWTManager = getattr(jwt_ext, 'JWTManager')
except Exception:
    class JWTManager:
        def __init__(self, app=None):
            if app is not None:
                app.logger.warning('flask_jwt_extended not installed; JWTManager is a no-op')

try:
    from flask_cors import CORS
except Exception:
    class CORS:
        def __init__(self, app=None, **kwargs):
            if app is not None:
                app.logger.warning('Flask-Cors not installed; CORS will not be applied')

from app.routes import user_bp

def create_app():
    app = Flask(__name__)
    # Load configuration from app.config.Config
    app.config.from_object('app.config.Config')
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = app.config.get('SECRET_KEY', 'dev-secret')
    JWTManager(app)
    
    # Initialize Swagger/OpenAPI docs with Bearer token support
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "Flask User CRUD API",
            "description": "A REST API for user management with JWT authentication",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Bearer token. Format: Bearer <token>"
            }
        },
        "security": [
            {"Bearer": []}
        ]
    }
    
    Flasgger(app, config=swagger_config, template=swagger_template)
    # Configure CORS for API endpoints. Default origins come from config or allow all.
    # Explicitly allow common methods and headers so preflight (OPTIONS) requests succeed.
    CORS(
        app,
        resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )
    
    # Register Blueprint
    app.register_blueprint(user_bp, url_prefix='/api')

    # register error handlers
    from app.helpers.errors import register_error_handlers
    register_error_handlers(app)
    
    return app
