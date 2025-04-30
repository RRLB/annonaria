from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
from flask_jwt_extended import JWTManager
import os


# Initialise 
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    #load environment variables
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Configure database
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

    # Initialise
    db.init_app(app)
    jwt.init_app(app)

    # add swagger
    Swagger(app)
    # Register blueprints (routes)
    from .routes.campaign import campaigns_bp #was app.routes
    from .routes.auth import auth_bp
    app.register_blueprint(campaigns_bp, url_prefix='/api/v1')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')

    # Create database tables 
    with app.app_context():
        db.create_all()

    return app
