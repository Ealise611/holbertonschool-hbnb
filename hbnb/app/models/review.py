#!/usr/bin/python3

from app.models.base_model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not place:
            raise ValueError("Place is required")
        if not user:
            raise ValueError("User is required")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
