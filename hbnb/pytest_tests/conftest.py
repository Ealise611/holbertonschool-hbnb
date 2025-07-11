"""
Pytest configuration
"""
import pytest
import os
import sys

# Add parent directory so we can import our app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Simple test config test database
class SimpleTestConfig:
    TESTING = True
    SECRET_KEY = 'simple-test-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/hbnb_test_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'simple-jwt-key'
    BCRYPT_LOG_ROUNDS = 4  # Faster password hashing for tests

@pytest.fixture
def app():
    """Create a simple test app using MySQL"""
    app = create_app(SimpleTestConfig)
    
    with app.app_context():
        # Test database connection
        try:
            result = db.session.execute(db.text('SELECT DATABASE()'))
            db_name = result.fetchone()[0]
            print(f" Connected to MySQL database: {db_name}")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
        
        # Create tables if they don't exist
        db.create_all()
        yield app

@pytest.fixture
def client(app):
    """Create test client for API requests"""
    return app.test_client()

@pytest.fixture
def clean_db(app):
    """Start each test with clean database"""
    with app.app_context():
        # Clean up existing test data before each test
        try:
            Review.query.delete()           # Reviews reference User and Place
            
            # Delete many-to-many association table data <<< to do
            try:
                db.session.execute(db.text('DELETE FROM place_amenity'))
            except:
                # Table might not exist yet so pass this
                pass
            
            Place.query.delete()            # Places reference User
            Amenity.query.delete()          # Amenities (no foreign keys)
            User.query.delete()             # Users (parent records)
            
            db.session.commit()
            print(" Database cleaned for test")
        except Exception as e:
            print(f" Database cleanup warning: {e}")
            db.session.rollback()
        
        yield db
        
        # Clean up after test too
        try:
            Review.query.delete()
            try:
                db.session.execute(db.text('DELETE FROM place_amenity'))
            except:
                pass
            Place.query.delete()
            Amenity.query.delete()
            User.query.delete()
            db.session.commit()
        except:
            db.session.rollback()