# models/user.py
# Defines the User model for the Annonaria backend using SQLAlchemy.
# This module specifies the schema for the 'users' database table and provides
# methods for secure password hashing and verification.

from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model): 
    """SQLAlchemy model representing a user in the Annonaria application."""
    # Implicitly maps to the 'users' table (SQLAlchemy uses lowercase plural by default)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        """Hash and store the user's password securely.
        
        Args:
            password (str): The plaintext password to hash.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a plaintext password against the stored hash.
        
        Args:
            password (str): The plaintext password to verify.
        
        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        return check_password_hash(self.password_hash, password)