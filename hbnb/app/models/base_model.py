#!/usr/bin/python3

import uuid
from datetime import datetime
from app import db

class BaseModel(db.Model):
    __abstract__ = True  # This makes it an abstract base class that won't create a table
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes based on input"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def delete(self):
        """Placeholder for deleting this object later"""
        pass
