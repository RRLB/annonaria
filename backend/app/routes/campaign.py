# routes/campaign.py
# Blueprint for campaign-related API endpoints in the Annonaria backend.
# Provides CRUD operations for campaigns and a toggle endpoint, with JWT authentication
# and Marshmallow schema validation for input/output serialization.

from flask import Blueprint, request, jsonify
from app.models.campaign import CampaignModel
from app.schemas.campaign import CampaignSchema, campaign_schema, multi_campaigns_schema
# from app.database import get_db_session
from app import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from marshmallow.exceptions import ValidationError 
from flasgger import swag_from
from flask_jwt_extended import jwt_required

# Define the campaigns blueprint for modular routing
campaigns_bp = Blueprint('campaigns', __name__)

#GET ALL - users can create campaigns
@campaigns_bp.route('/campaigns', methods=['GET'])
@jwt_required()
@swag_from({
     'security': [{'BearerAuth': []}],
    'responses': {
        200: {
            'description': 'List of all campaigns',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'description': {'type': 'string'},
                        'start_date': {'type': 'string', 'format': 'date'},
                        'end_date': {'type': 'string', 'format': 'date'},
                        'budget': {'type': 'number'},
                        'is_active': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def get_multi_campaigns():
    """Retrieve a list of all campaigns.
    
    Requires JWT authentication. Returns serialized campaign data.
    
    Returns:
        JSON response with a list of campaigns and HTTP status 200.
    """
    campaigns = CampaignModel.query.all()
    return jsonify(multi_campaigns_schema.dump(campaigns)), 200

#POST create campaigne - users can create campaigns
@campaigns_bp.route('/campaigns', methods=['POST'])
@jwt_required()
@swag_from({
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'Test Campaign'},
                    'description': {'type': 'string', 'example': 'A test campaign'},
                    'start_date': {'type': 'string', 'format': 'date', 'example': '2026-01-01'},
                    'end_date': {'type': 'string', 'format': 'date', 'example': '2026-12-31'},
                    'budget': {'type': 'number', 'example': 10000.0},
                    'is_active': {'type': 'boolean', 'example': False}
                },
                'required': ['name', 'start_date', 'end_date', 'budget']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Campaign created',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'start_date': {'type': 'string', 'format': 'date'},
                    'end_date': {'type': 'string', 'format': 'date'},
                    'budget': {'type': 'number'},
                    'is_active': {'type': 'boolean'}
                }
            }
        },
        400: {
            'description': 'Invalid input',
            'schema': {
                'type': 'object',
                'properties': {
                    'errors': {'type': 'object'}
                }
            }
        }
    }
})
def create_campaign():
    """Create a new campaign.
    
    Requires JWT authentication. Validates input using CampaignSchema and stores
    the campaign in the database.
    
    Returns:
        JSON response with the created campaign and HTTP status 201, or an error
        with status 400 if validation or database constraints fail.
    """
    data = request.get_json()
    
    try:
        # Validate and deserialize input
        schema = campaign_schema
        if 'start_date' in data:
            schema.context['start_date'] = schema.fields['start_date'].deserialize(data['start_date'])
        campaign_data = schema.load(data, partial=('id',))
        campaign = CampaignModel(**campaign_data)
        db.session.add(campaign)
        db.session.commit()
        return jsonify(campaign_schema.dump(campaign)), 201
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Campaign creation failed'}), 400

#GET one - anyone can see one campaign with the right id/link
@campaigns_bp.route('/campaigns/<int:id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the campaign to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Campaign found',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'start_date': {'type': 'string', 'format': 'date'},
                    'end_date': {'type': 'string', 'format': 'date'},
                    'budget': {'type': 'number'},
                    'is_active': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Campaign not found'
        }
    }
})
def get_campaign(id):
    """Retrieve a single campaign by ID.
    
    No authentication required. Returns the serialized campaign data.
    
    Args:
        id (int): The ID of the campaign to retrieve.
    
    Returns:
        JSON response with the campaign and HTTP status 200, or an error with
        status 404 if the campaign is not found.
    """
    campaign = db.session.query(CampaignModel).get(id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    return jsonify(campaign_schema.dump(campaign)), 200

#PUT update - users can create campaigns
@campaigns_bp.route('/campaigns/<int:id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the campaign to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'},
                    'start_date': {'type': 'string', 'format': 'date'},
                    'end_date': {'type': 'string', 'format': 'date'},
                    'budget': {'type': 'number'},
                    'is_active': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Campaign updated successfully'
        },
        400: {
            'description': 'Validation error or update failed'
        },
        404: {
            'description': 'Campaign not found'
        }
    }
})
def update_campaign(id):
    """Update an existing campaign by ID.
    
    Requires JWT authentication. Validates input using CampaignSchema and updates
    the campaign in the database.
    
    Args:
        id (int): The ID of the campaign to update.
    
    Returns:
        JSON response with the updated campaign and HTTP status 200, or an error
        with status 404 (not found) or 400 (validation/database error).
    """
    campaign = db.session.query(CampaignModel).get(id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    data = request.get_json()
    try:
        # Validate and deserialize input
        schema = campaign_schema
        if 'start_date' in data:
            schema.context['start_date'] = schema.fields['start_date'].deserialize(data['start_date'])
        campaign_data = schema.load(data, partial=('id',))
        for key, value in campaign_data.items():
            setattr(campaign, key, value)
        db.session.commit()
        return jsonify(campaign_schema.dump(campaign)), 200
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Campaign update failed'}), 400

#DELETE - users can create campaigns
@campaigns_bp.route('/campaigns/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'security': [{'BearerAuth': []}],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the campaign to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Campaign deleted'
        },
        404: {
            'description': 'Campaign not found'
        }
    }
})
def delete_campaign(id):
    """Delete a campaign by ID.
    
    Requires JWT authentication.
    
    Args:
        id (int): The ID of the campaign to delete.
    
    Returns:
        JSON response with a success message and HTTP status 200, or an error
        with status 404 if the campaign is not found.
    """
    campaign = db.session.query(CampaignModel).get(id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    db.session.delete(campaign)
    db.session.commit()
    return jsonify({'message': 'Campaign deleted'}), 200

#PATCH update - users can create campaigns
@campaigns_bp.route('/campaigns/<int:id>/toggle', methods=['PATCH'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of the campaign to toggle'
        }
    ],
    'responses': {
        200: {
            'description': 'Campaign toggled',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'is_active': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Campaign not found'
        }
    }
})
def toggle_campaign(id):
    """Toggle the active status of a campaign by ID.
    
    No authentication required. Switches the campaign's is_active field between
    True and False.
    
    Args:
        id (int): The ID of the campaign to toggle.
    
    Returns:
        JSON response with the updated campaign and HTTP status 200, or an error
        with status 404 if the campaign is not found.
    """
    campaign = db.session.query(CampaignModel).get(id)
    if not campaign:
        return jsonify({'error': 'Campaign not found'}), 404
    
    campaign.is_active = not campaign.is_active
    db.session.commit()
    return jsonify(campaign_schema.dump(campaign)), 200