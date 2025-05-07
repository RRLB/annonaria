# schemas/users.py
# Marshmallow schema for validating and serializing user data in the Annonaria backend.
# Defines the UserSchema for use in user-related API endpoints, such as GET /api/v1/users.

from marshmallow import Schema, fields

class UserSchema(Schema):
    """Schema for validating and serializing User model data.
    
    Used primarily for output serialization in the GET /api/v1/users endpoint to
    return user data (id and username) in a JSON-compatible format.
    """
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

# Schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)