#!/usr/bin/env python3
"""
Database reset script for HBnB project
Usage: python reset_db.py
"""

from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
import uuid

def reset_database():
    """Reset the database and add initial data"""
    app = create_app()
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Adding initial data...")
        
        # Create admin user
        admin = User(
            id='36c9050e-ddd3-4c3b-9731-9f487208bbc1',
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            is_admin=True
        )
        admin.hash_password('admin1234')
        db.session.add(admin)
        
        # Create initial amenities
        amenities = [
            Amenity(name='WiFi'),
            Amenity(name='Swimming Pool'),
            Amenity(name='Air Conditioning')
        ]
        
        for amenity in amenities:
            db.session.add(amenity)
        
        try:
            db.session.commit()
            print("Database reset completed successfully!")
            print("Admin user created: admin@hbnb.io / admin1234")
            print("Initial amenities added: WiFi, Swimming Pool, Air Conditioning")
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")

if __name__ == '__main__':
    reset_database()