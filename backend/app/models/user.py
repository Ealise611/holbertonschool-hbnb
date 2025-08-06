#!/usr/bin/python3

import re
import uuid
from app.models.base_model import BaseModel
from app import db


class User(BaseModel):
    # create table for user
    __tablename__ = 'users'
    # Define SQLAlchemy columns for the User model
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    #define relationships for user
    places = db.relationship('Place', back_populates='owner', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        # Validate and clean inputs
        if not first_name or not first_name.strip():
            raise ValueError("First name is required and be ≤ 50 characters")
        if len(first_name.strip()) > 50:
            raise ValueError("First name is required and be ≤ 50 characters")

        if not last_name or not last_name.strip():
            raise ValueError("Last name is required and be ≤ 50 characters")
        if len(last_name.strip()) > 50:
            raise ValueError("Last name is required and be ≤ 50 characters")

        if not email or not email.strip():
            raise ValueError("Invalid email")
        if not self._is_valid_email(email.strip()):
            raise ValueError("Invalid email")

        if not password or not password.strip():
            raise ValueError("Password cannot be empty")

        # Store cleaned values
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin
        
        self.hash_password(password)
            
    def hash_password(self, password):
        '''Hashes the password before storing it'''
        from app import bcrypt # Imports bcrypt INSIDE the method to avoid circular imports
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")
        # hashes the password
        self.password = bcrypt.generate_password_hash(password.strip()).decode('utf-8')
        
    def verify_password(self, password):
        '''Checks if password matches stored hash'''
        from app import bcrypt
        if not password or not self.password:
            return False
        # compares the hash to input password
        return bcrypt.check_password_hash(self.password, password.strip())

    def _is_valid_email(self, email):
        if not email or not email.strip():
            return False
        return re.match(r"[^@]+@[^@]+\.[^@]+", email.strip()) is not None