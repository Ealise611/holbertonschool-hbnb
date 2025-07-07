"""
Additional pytest fixtures for comprehensive testing
"""
import pytest
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from flask_jwt_extended import create_access_token

@pytest.fixture
def sample_user(clean_db, app):
    """Create a sample user in MySQL"""
    with app.app_context():
        user = User(
            first_name="Pytest",
            last_name="User",
            email="pytest.user@mysql.test",
            is_admin=False
        )
        user.hash_password("pytestpass123")
        
        clean_db.session.add(user)
        clean_db.session.commit()
        clean_db.session.refresh(user)
        
        print(f"✅ Created sample user: {user.email} (ID: {user.id})")
        return user

@pytest.fixture
def admin_user(clean_db, app):
    """Create an admin user in MySQL"""
    with app.app_context():
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
        
        print(f"✅ Created admin user: {admin.email} (ID: {admin.id})")
        return admin

@pytest.fixture
def user_token(app, sample_user):
    """Generate JWT token for regular user"""
    with app.app_context():
        token = create_access_token(
            identity={'id': str(sample_user.id), 'is_admin': False}
        )
        return token

@pytest.fixture
def admin_token(app, admin_user):
    """Generate JWT token for admin user"""
    with app.app_context():
        token = create_access_token(
            identity={'id': str(admin_user.id), 'is_admin': True}
        )
        return token

@pytest.fixture
def auth_headers():
    """Helper to create authorization headers"""
    def _create_headers(token):
        return {'Authorization': f'Bearer {token}'}
    return _create_headers