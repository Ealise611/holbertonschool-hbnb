#!/usr/bin/python3

import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base model class for all models in the application."""
    __abstract__ = True  # This class will not create a table in the database
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)


    def save(self):
        self.updated_at = datetime.now()
        db.session.commit()

    def update(self, data):
        """Update attributes based on input"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Delete this object from the database."""
        db.session.delete(self)
        db.session.commit()
