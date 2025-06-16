#!/usr/bin/python3

from models import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required and be ≤ 50 characters")

        self.name = name
        self.description = description
