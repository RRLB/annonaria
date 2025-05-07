# models/campaign.py
# Defines the CampaignModel for the Annonaria backend using SQLAlchemy.
# This module specifies the schema for the 'campaigns' database table and provides
# a method to serialize campaign data for API responses.

from app import db
from datetime import date

class CampaignModel(db.Model):
    """SQLAlchemy model representing a campaign in the Annonaria application."""
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True) 

    # to dictionary
    def to_dict(self):
        """
        Serialize the campaign instance to a dictionary for API responses.
        
        Returns:
            dict: A dictionary containing the campaign's attributes with dates
                  formatted as ISO strings (e.g., '2023-10-01').
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'budget': self.budget,
            'is_active': self.is_active
        }


