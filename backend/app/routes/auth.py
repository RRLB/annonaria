from flask import Blueprint, request, jsonify
from app import db
from app.models.users import User
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from app.schemas.users import users_schema
from flask_jwt_extended import get_jwt_identity, jwt_required

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
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registerd'}), 201

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
        403: {
            'description': 'Forbidden – admin access required'
        },
        401: {
            'description': 'Missing or invalid JWT token'
        }
    }
})
def get_all_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user :
        return jsonify({'message': 'Access forbidden: Admins only'}), 403
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200