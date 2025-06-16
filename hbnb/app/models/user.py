#!/usr/bin/python3

import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and be ≤ 50 characters")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and be ≤ 50 characters")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")
        if not password:
            raise ValueError("Password required")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password  # Should this be hashed?
        self.is_admin = is_admin

    def _is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
    
