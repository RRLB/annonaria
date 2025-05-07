# app/__init__.py
# Factory function to create and configure the Flask application for the Annonaria backend.
# This module initializes the Flask app, sets up extensions (database, JWT, CORS, Swagger),
# registers routes, and creates database tables.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
from flask_jwt_extended import JWTManager
import os

# Initialize Flask extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    """Create and configure the Flask application instance."""
    #load environment variables
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Configure Flask app settings
    # Database URI from environment variable
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') #os.urandom(24).hex()
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['SWAGGER'] = {
        'title': 'Annonaria Campaign API',
        'uiversion': 3,
        'openapi': '3.0.3',
        'components': {
            'securitySchemes': {
                'BearerAuth': {
                    'type': 'http',
                    'scheme': 'bearer',
                    'bearerFormat': 'JWT'
                }
            }
        }
    }

    # Initialise Flask extensions
    db.init_app(app)
    jwt.init_app(app)

    # add swagger for interactive API documentation
    Swagger(app)
    # Register blueprints for modular route handling
    # Campaigns blueprint handles campaign-related endpoints (e.g., /api/v1/campaigns)
    from .routes.campaign import campaigns_bp
    # Auth blueprint handles authentication endpoints (e.g., /api/v1/register, /api/v1/login)
    from .routes.auth import auth_bp
    app.register_blueprint(campaigns_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')

    # Create database tables 
    with app.app_context():
        db.create_all()

    return app
