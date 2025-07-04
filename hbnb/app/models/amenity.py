#!/usr/bin/python3

import uuid
from app.models.base_model import BaseModel
from app.models.place import place_amenity
from app import db

def generate_uuid():
    """Generates a unique identifier for the amenity."""
    return str(uuid.uuid4())

class Amenity(BaseModel):
    # Define SQLAlchemy columns for the Amenity model
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    # Define relationships
    places = db.relationship('Place', secondary=place_amenity, back_populates='amenities')


    def __init__(self, name, description=""):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and be ≤ 50 characters")

        self.name = name
        self.description = description
