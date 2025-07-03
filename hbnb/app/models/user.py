#!/usr/bin/python3

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False): # TODO remove =None later
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
        
        if password is not None and (not password or not password.strip()):
            raise ValueError("Password cannot be empty")
            
        if not email or not email.strip():
            raise ValueError("Invalid email")
        if not self._is_valid_email(email.strip()):
            raise ValueError("Invalid email")

        if password and not password.strip(): 
            raise ValueError("Password cannot be empty")

        # Store cleaned values
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin
        
        if password:
            self.hash_password(password)
        else:
            self.password = None
            
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

    def hash_password(self, password):
        """Hash the password before storing it. """
        from app import bcrypt
        if not password or not password.strip():
            raise ValueError("Password cannot be empty")
        self.password = bcrypt.generate_password_hash(password.strip()).decode('utf-8')

    def verify_password(self, password):
        """Verify if the provided password matches the hashed password. """
        from app import bcrypt
        if not password or not password.strip():
            return False
        return bcrypt.check_password_hash(self.password, password.strip())
