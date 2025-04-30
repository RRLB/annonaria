# using marshmallow for validation
from marshmallow import Schema, fields, validates, ValidationError
from datetime import date
import logging

# Configure logging to debug validation
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CampaignSchema(Schema):
    id = fields.Int(dump_only=True) # Read-only for responses
    name = fields.Str(required=True, validate=lambda x: len(x) <= 100)
    description = fields.Str(allow_none=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)
    budget = fields.Float(required=True)
    is_active = fields.Boolean(default=True)

    # data validation // basic checks for end date and budget
    @validates('end_date')
    def validate_end_date(self, value):
        logger.debug(f"Validating end_date: {value}")
        if value < date.today():
            logger.error(f"End date {value} is in the past")
            raise ValidationError('End date cannot be in the past.')
        if 'start_date' in self.context:
            start_date = self.context['start_date']
            logger.debug(f"Comparing end_date {value} with start_date {start_date}")
            if value < start_date:
                logger.error(f"End date {value} is before start_date {start_date}")
                raise ValidationError('End date must be after start date.')
        else:
            logger.warning("start_date not found in context during end_date validation")

    @validates('budget')
    def validate_budget(self, value):
        if value <= 0:
            raise ValidationError('Budget must be positive.')
        
# Instances for different use cases
campaign_schema = CampaignSchema() # For single campaign
multi_campaigns_schema = CampaignSchema(many=True) # For list of campaigns