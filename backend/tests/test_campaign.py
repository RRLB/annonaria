import pytest
import json
from app import db
from app.models.campaign import CampaignModel
from datetime import date, timedelta

def test_create_campaign_success(client, auth_headers):
    # Fixed past start date
    start_date = date(2024, 4, 1)

    # end_date must still be in the future relative to today
    end_date = date.today() + timedelta(days=30) #sets end date 30 days after

    campaign_data = {
        'name': 'Testing Campaign 101',
        'description': 'A test campaign',
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'budget': 10000.0, #float
        'is_active': True
    }
    response = client.post('/api/v1/campaigns', json=campaign_data, headers=auth_headers)
    assert response.status_code == 201, f"Failed with {response.json}"
    data = response.json
    assert data['name'] == 'Testing Campaign 101'
    assert data['budget'] == 10000.0
    assert data['is_active'] is True
    with client.application.app_context():
        assert CampaignModel.query.count() == 1

def test_create_campaign_invalid_dates(client, auth_headers):
    campaign_data = {
        'name': 'Invalid Campaign',
        'description': 'Test',
        'start_date': '2026-06-12',
        'end_date': '2025-11-10', # End before start
        'budget': 100000.0,
        'is_active': False
    }
    response = client.post('/api/v1/campaigns', json=campaign_data, headers=auth_headers)
    assert response.status_code == 400, f"Failed with {response.json}"
    assert 'end_date' in response.json['errors']
    assert 'End date must be after start date.' in response.json['errors']['end_date']  # Check list membership

def test_create_campaign_unauthorized(client):
    campaign_data = {
        'name': 'Testing Campaign 101',
        'description': 'A test campaign',
        'start_date': '2025-04-01',
        'end_date': '2025-10-14',
        'budget': 10000.0,
        'is_active': True
    }
    response = client.post('/api/v1/campaigns', json=campaign_data)
    assert response.status_code == 401
    assert response.json == {'msg': 'Missing Authorization Header'}

def test_get_campaigns_success(client, auth_headers):
    with client.application.app_context():
        campaign = CampaignModel(
            name = 'Test Campaign',
            description = 'Test',
            start_date = date(2025, 1, 1),
            end_date = date(2025, 12, 31),
            budget = 10000.0,
            is_active = True
        )
        db.session.add(campaign)
        db.session.commit()
    response = client.get('/api/v1/campaigns', headers=auth_headers)
    assert response.status_code == 200, f"Failed with {response.json}"
    data = response.json
    assert len(data) == 1
    assert data[0]['name'] == 'Test Campaign'