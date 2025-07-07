"""
Test User functionality with MySQL and pytest
"""
import pytest
import json

@pytest.mark.mysql
class TestUserWithMySQL:
    """Test User model and API with MySQL"""
    
    def test_user_creation_in_mysql(self, clean_db, app):
        """Test creating a user directly in MySQL"""
        with app.app_context():
            from app.models.user import User
            
            user = User(
                first_name="MySQL",
                last_name="Tester",
                email="mysql.test@pytest.com"
            )
            user.hash_password("mysqlpass123")
            
            clean_db.session.add(user)
            clean_db.session.commit()
            
            # Verify user was saved to MySQL
            saved_user = clean_db.session.query(User).filter_by(email="mysql.test@pytest.com").first()
            assert saved_user is not None
            assert saved_user.first_name == "MySQL"
            assert saved_user.verify_password("mysqlpass123")
            
            print(f"✅ User saved to MySQL with ID: {saved_user.id}")
    
    def test_user_api_with_mysql(self, client, clean_db):
        """Test user registration API with MySQL backend"""
        user_data = {
            "first_name": "API",
            "last_name": "User",
            "email": "api.user@pytest.com",
            "password": "apipass123"
        }
        
        response = client.post('/api/v1/users/', json=user_data)
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['email'] == "api.user@pytest.com"
        assert 'password' not in data
        
        # Verify user was actually saved in MySQL
        with clean_db.session.no_autoflush:
            from app.models.user import User
            saved_user = clean_db.session.query(User).filter_by(email="api.user@pytest.com").first()
            assert saved_user is not None
            assert saved_user.verify_password("apipass123")
        
        print("✅ User API registration saved to MySQL")
    
    def test_duplicate_email_mysql_constraint(self, client, clean_db):
        """Test that MySQL enforces unique email constraint"""
        user_data = {
            "first_name": "First",
            "last_name": "User",
            "email": "duplicate@pytest.com",
            "password": "pass1"
        }
        
        # Create first user
        response1 = client.post('/api/v1/users/', json=user_data)
        assert response1.status_code == 201
        
        # Try to create second user with same email
        user_data["first_name"] = "Second"
        response2 = client.post('/api/v1/users/', json=user_data)
        assert response2.status_code == 400
        
        data = json.loads(response2.data)
        assert 'already registered' in data['error'].lower()
        print("✅ MySQL unique constraint working via API")

@pytest.mark.mysql
class TestAuthenticationWithMySQL:
    """Test authentication with MySQL backend"""
    
    def test_login_with_mysql_user(self, client, sample_user):
        """Test login with user stored in MySQL"""
        login_data = {
            "email": "pytest.user@mysql.test",
            "password": "pytestpass123"
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'access_token' in data
        assert len(data['access_token']) > 10
        print("✅ Login successful with MySQL user")
    
    def test_protected_endpoint_with_mysql(self, client, user_token, auth_headers):
        """Test protected endpoint with MySQL-backed authentication"""
        place_data = {
            "title": "MySQL Test Place",
            "description": "Created with MySQL backend",
            "price": 200.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": []
        }
        
        response = client.post(
            '/api/v1/places/',
            json=place_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == "MySQL Test Place"
        print("✅ Protected endpoint works with MySQL authentication")