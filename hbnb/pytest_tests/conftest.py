"""
Pytest configuration with dedicated MySQL test database
"""
import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from flask_jwt_extended import create_access_token

@pytest.fixture(scope='session')
def app():
    """Create test app with dedicated TestingConfig"""
    print("\n🧪 [PYTEST] Creating test app with TestingConfig...")
    
    # Use TestingConfig which points to hbnb_test_db
    app = create_app('TestingConfig')
    
    with app.app_context():
        try:
            # Verify we're connected to the test database
            with db.engine.connect() as conn:
                result = conn.execute(db.text('SELECT DATABASE()'))
                db_name = result.fetchone()[0]
                print(f"✅ Connected to test database: {db_name}")
                
                # Ensure it's the test database
                assert db_name == 'hbnb_test_db', f"Expected hbnb_test_db, got {db_name}"
            
            print("✅ Test database connection verified")
            yield app
            
            print("🧹 Test session cleanup completed")
            
        except Exception as e:
            print(f"❌ Test app setup failed: {e}")
            raise

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def clean_db(app):
    """Clean database before each test"""
    with app.app_context():
        try:
            print("🧹 Cleaning test database...")
            
            # Disable foreign key checks for cleanup
            db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 0'))
            
            # Clean all tables
            db.session.execute(db.text('DELETE FROM place_amenity'))
            db.session.execute(db.text('DELETE FROM reviews'))
            db.session.execute(db.text('DELETE FROM places'))
            db.session.execute(db.text('DELETE FROM users'))
            db.session.execute(db.text('DELETE FROM amenities'))
            
            # Re-enable foreign key checks
            db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 1'))
            
            db.session.commit()
            print("✅ Database cleaned")
            
            yield db
            
        except Exception as e:
            print(f"❌ Database cleanup failed: {e}")
            db.session.rollback()
            raise

@pytest.fixture
def sample_user(clean_db, app):
    """Create a sample user in test database"""
    with app.app_context():
        print("🔧 Creating sample user...")
        user = User(
            first_name="Test",
            last_name="User",
            email="test.user@pytest.com",
            is_admin=False
        )
        user.hash_password("testpass123")
        
        clean_db.session.add(user)
        clean_db.session.commit()
        clean_db.session.refresh(user)
        
        print(f"✅ Created test user: {user.email} (ID: {user.id})")
        return user

@pytest.fixture
def admin_user(clean_db, app):
    """Create an admin user in test database"""
    with app.app_context():
        print("🔧 Creating admin user...")
        admin = User(
            first_name="Test",
            last_name="Admin",
            email="test.admin@pytest.com",
            is_admin=True
        )
        admin.hash_password("testadmin123")
        
        clean_db.session.add(admin)
        clean_db.session.commit()
        clean_db.session.refresh(admin)
        
        print(f"✅ Created test admin: {admin.email} (ID: {admin.id})")
        return admin

@pytest.fixture
def user_token(app, sample_user):
    """Generate JWT token for regular user"""
    with app.app_context():
        print("🔧 Creating user token...")
        token = create_access_token(
            identity={'id': str(sample_user.id), 'is_admin': False}
        )
        print("✅ User token created")
        return token

@pytest.fixture
def admin_token(app, admin_user):
    """Generate JWT token for admin user"""
    with app.app_context():
        print("🔧 Creating admin token...")
        token = create_access_token(
            identity={'id': str(admin_user.id), 'is_admin': True}
        )
        print("✅ Admin token created")
        return token

@pytest.fixture
def auth_headers():
    """Helper function to create authorization headers"""
    def _create_headers(token):
        return {'Authorization': f'Bearer {token}'}
    return _create_headers

@pytest.fixture
def sample_amenity(clean_db, app):
    """Create a sample amenity for testing"""
    with app.app_context():
        amenity = Amenity(
            name="Test Amenity",
            description="An amenity for testing"
        )
        clean_db.session.add(amenity)
        clean_db.session.commit()
        clean_db.session.refresh(amenity)
        
        print(f"✅ Created test amenity: {amenity.name} (ID: {amenity.id})")
        return amenity

@pytest.fixture
def sample_place(clean_db, sample_user, app):
    """Create a sample place for testing"""
    with app.app_context():
        from app.models.place import Place
        
        place = Place(
            title="Test Place",
            description="A place for testing",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=sample_user
        )
        clean_db.session.add(place)
        clean_db.session.commit()
        clean_db.session.refresh(place)
        
        print(f"✅ Created test place: {place.title} (ID: {place.id})")
        return place