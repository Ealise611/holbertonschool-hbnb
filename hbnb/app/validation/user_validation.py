# app/validation/user_validation.py

import re

def validate_user_data(data):
    required_fields = ['first_name', 'last_name', 'email']

    for field in required_fields:
        if field not in data or not isinstance(data[field], str) or not data[field].strip():
            raise ValueError(f"{field.replace('_', ' ').title()} is required and must be a non-empty string")

    email = data['email']
    email_regex = r'^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$'
    if not re.match(email_regex, email):
        raise ValueError("Email must be a valid email address")
