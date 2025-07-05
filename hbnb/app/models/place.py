import uuid
from app.models.base_model import BaseModel
from app.models.pivot_table import place_amenity
from app import db

class Place(BaseModel):
    #create table for place
    __tablename__ = 'places'
    # Define SQLAlchemy columns for the Place model
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Define relationships
    owner = db.relationship('User', back_populates='places')
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity, back_populates='places')


    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be ≤ 100 characters")
        if price < 0:
            raise ValueError("Price must be a positive number")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        if not owner:
            raise ValueError("Owner (User) is required")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.owner_id = owner.id

    def add_review(self, review):
        self.reviews.append(review)
    def add_amenity(self, amenity):
        self.amenities.append(amenity)