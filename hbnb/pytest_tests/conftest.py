"""
Complete pytest configuration with all needed fixtures
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
from flask_jwt_extended import create_access_token

class MySQLTestConfig:
    """MySQL test configuration"""
    SECRET_KEY = 'pytest-mysql-test-secret'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/hbnb_pytest_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'pytest-mysql-jwt-secret'

@pytest.fixture(scope='session')
def app():
    """Create test app with MySQL"""
    print("\n🗄️ [PYTEST-MYSQL] Creating test app...")
    app = create_app(MySQLTestConfig)
    
    with app.app_context():
        try:
            # Test connection
            with db.engine.connect() as conn:
                result = conn.execute(db.text('SELECT DATABASE()'))
                db_name = result.fetchone()[0]
                print(f"✅ Connected to: {db_name}")
            
            # Create tables
            db.create_all()
            print("✅ Tables created")
            yield app
            
        except Exception as e:
            print(f"❌ Error: {e}")
            raise

@pytest.fixture(scope='function')
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope='function')
def clean_db(app):
    """Clean database for each test"""
    with app.app_context():
        try:
            # Clear all data
            db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 0'))
            db.session.execute(db.text('DELETE FROM users'))
            db.session.execute(db.text('DELETE FROM amenities'))
            db.session.execute(db.text('DELETE FROM places'))
            db.session.execute(db.text('SET FOREIGN_KEY_CHECKS = 1'))
            db.session.commit()
            yield db
        except Exception as e:
            print(f"❌ Database cleanup failed: {e}")
            db.session.rollback()
            raise

# ADD THESE MISSING FIXTURES:

@pytest.fixture
def sample_user(clean_db, app):
    """Create a sample user in MySQL - THIS WAS MISSING!"""
    with app.app_context():
        print("🔧 Creating sample user...")
        user = User(
            first_name="Pytest",
            last_name="User",
            email="pytest.user@mysql.test",
            is_admin=False
        )
        user.hash_password("pytestpass123")
        
        clean_db.session.add(user)
        clean_db.session.commit()
        clean_db.session.refresh(user)  # Get ID from database
        
        print(f"✅ Created user: {user.email} (ID: {user.id})")
        return user

@pytest.fixture
def admin_user(clean_db, app):
    """Create an admin user in MySQL"""
    with app.app_context():
        print("🔧 Creating admin user...")
        admin = User(
            first_name="Pytest",
            last_name="Admin",
            email="pytest.admin@mysql.test",
            is_admin=True
        )
        admin.hash_password("pytestadmin123")
        
        clean_db.session.add(admin)
        clean_db.session.commit()
        clean_db.session.refresh(admin)
        
        print(f"✅ Created admin: {admin.email} (ID: {admin.id})")
        return admin

@pytest.fixture
def user_token(app, sample_user):
    """Generate JWT token for regular user - THIS WAS MISSING!"""
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
    """Helper function to create authorization headers - THIS WAS MISSING!"""
    def _create_headers(token):
        return {'Authorization': f'Bearer {token}'}
    return _create_headers