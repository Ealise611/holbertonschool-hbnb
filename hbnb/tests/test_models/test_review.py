#!/usr/bin/env python3
"""Test Review model"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.user import User
from app.models.place import Place
from app.models.review import Review

def test_review_creation():
    user = User(first_name="Bob", last_name="Wilson", email="bob@example.com", password="password123")
    place = Place(title="Nice House", description="Great place", price=150, latitude=40.7128, longitude=-74.0060, owner=user)
    
    review = Review(text="Excellent stay!", rating=4, place=place, user=user)
    
    assert review.text == "Excellent stay!"
    assert review.rating == 4
    assert review.place == place
    assert review.user == user
    print("Review creation test passed!")

if __name__ == "__main__":
    test_review_creation()