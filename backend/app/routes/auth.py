# routes/auth.py
# Blueprint for authentication-related API endpoints in the Annonaria backend.
# Provides endpoints for user registration, login, and retrieving all users,
# using JWT for authentication and Marshmallow for user data serialization.

from flask import Blueprint, request, jsonify
from app import db
from app.models.users import User
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from app.schemas.users import users_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

# Define the auth blueprint for modular routing
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'username': {'type': 'string', 'example': 'user1'},
                    'password': {'type': 'string', 'example': 'password123'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered'},
        400: {'description': 'Username already exists'}
    }
})
def register():
    """Register a new user and return a JWT access token.
    
    Expects a JSON payload with username and password. Creates a new user with
    a hashed password and returns a JWT token for authentication.
    
    Returns:
        JSON response with the access token and HTTP status 201, or an error
        with status 400 if the username already exists.
    """
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    #create token
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 201

@auth_bp.route('/login', methods=['POST'])
@swag_from({
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'example': 'user1'},
                    'password': {'type': 'string', 'example': 'password123'}
                },
                'required': ['username', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'access_token': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Invalid credentials'}
    }
})
def login():
    """Authenticate a user and return a JWT access token.
    
    Expects a JSON payload with username and password. Verifies credentials
    and returns a JWT token if valid.
    
    Returns:
        JSON response with the access token and HTTP status 200, or an error
        with status 401 if credentials are invalid.
    """
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@swag_from({
    'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'List of all users',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'username': {'type': 'string'}
                    }
                }
            }
        },
        401: {
            'description': 'Missing or invalid JWT token'
        }
    }
})
def get_all_users():
    """Retrieve a list of all users.
    
    Requires JWT authentication.
    
    Returns:
        JSON response with a list of users and HTTP status 200, or an error
        with status 403 if access is forbidden.
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user :
        return jsonify({'message': 'Access forbidden: Admins only'}), 403
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200