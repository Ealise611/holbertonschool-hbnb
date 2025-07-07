#!/usr/bin/python3

import uuid
from app.models.base_model import BaseModel
from app import db

class Review(BaseModel):
    # create table for review
    __tablename__ = 'reviews'

    # Define SQLAlchemy columns for the Review model
    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    # Define relationships
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')

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
        self.place_id = place.id
        self.user_id = user.id
