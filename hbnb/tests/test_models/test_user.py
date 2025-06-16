#!/usr/bin/env python3
"""Test User model"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password123")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.is_admin is False
    print("User creation test passed!")

if __name__ == "__main__":
    test_user_creation()
