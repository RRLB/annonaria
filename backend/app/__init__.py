from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
from flasgger import Swagger
import os

# Initialise SQLAlchemy
db = SQLAlchemy()

def create_app():
    #load environment variables
    load_dotenv()

    app = Flask(__name__)
    CORS(app)

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise database
    db.init_app(app)

    # add swagger
    Swagger(app)
    # Register blueprints (routes)
    from app.routes.campaign import campaigns_bp
    app.register_blueprint(campaigns_bp, url_prefix='/api/v1')

    # Create database tables 
    with app.app_context():
        db.create_all()

    return app
