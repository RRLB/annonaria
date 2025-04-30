# SQLAlchemy module
from app import db
from datetime import date

class CampaignModel(db.Model):
    __tablename__ = 'campaigns'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True) #default True or False @todo

    # to dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'budget': self.budget,
            'is_active': self.is_active
        }
    
# Method: to_dict() simplifies serialization for API responses.

