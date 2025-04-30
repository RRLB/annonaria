import pytest
from app import create_app
from app.models.campaign import CampaignModel
from datetime import date

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_campaign(client):
    campaign_data = {
        'name': 'Testing Campaign 101',
        'description': 'A test campaign',
        'start_date': '2025-04-01',
        'end_date': '2025-10-14',
        'budget': 10000,
        'is_active': True
    }
    response = client.post('/api/v1/campaigns', json=campaign_data)
    assert response.status_code == 201
    assert response.json['name'] == 'Testing Campaign 101'
    assert response.json['budget'] == 10000