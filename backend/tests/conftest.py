import pytest 
from app import create_app, db
from app.models.users import User
from flask_jwt_extended import create_access_token

#pytest decorator -> marks function app() as a fixture
@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key' #consistent for tests
    #context manager that sets up the Flask application
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()
@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(app, client):
    with app.app_context():
        user = User(username='testuser')
        user.set_password('testpass123')
        db.session.add(user)
        db.session.commit()
        token = create_access_token(identity=str(user.id)) 
        return {'Authorization' : f'Bearer {token}'}