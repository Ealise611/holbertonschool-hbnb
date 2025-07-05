#!/usr/bin/python3

import uuid
from app.models.base_model import BaseModel
from app.models.pivot_table import place_amenity
from app import db

class Amenity(BaseModel):
    #create table for amenity
    __tablename__ = 'amenities'

    # Define SQLAlchemy columns for the Amenity model
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
