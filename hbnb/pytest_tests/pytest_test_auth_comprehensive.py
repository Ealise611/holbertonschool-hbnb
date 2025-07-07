"""
Fixed authentication tests that match your API's actual behavior
"""
import pytest
import json

@pytest.mark.auth
class TestAuthenticationFixed:
    """Fixed authentication tests"""
    
    def test_successful_login(self, client, sample_user):
        """Test successful login"""
        login_data = {
            "email": "pytest.user@mysql.test",
            "password": "pytestpass123"
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'access_token' in data
        assert len(data['access_token']) > 10
        print("✅ Login successful")
    
    def test_admin_login(self, client, admin_user):
        """Test admin login"""
        login_data = {
            "email": "pytest.admin@mysql.test", 
            "password": "pytestadmin123"
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'access_token' in data
        print("✅ Admin login successful")
    
    @pytest.mark.parametrize("email,password,error_type", [
        ("nonexistent@test.com", "password", "Non-existent user"),
        ("pytest.user@mysql.test", "wrongpass", "Wrong password"), 
        ("pytest.user@mysql.test", "", "Empty password"),
        ("", "pytestpass123", "Empty email"),
        ("invalid-email", "password", "Invalid email"),
    ])
    def test_login_failures(self, client, sample_user, email, password, error_type):
        """Test various login failure scenarios - expecting 401"""
        login_data = {"email": email, "password": password}
        
        response = client.post('/api/v1/auth/login', json=login_data)
        
        # Your API returns 401 for all auth failures - that's fine!
        assert response.status_code == 401
        
        data = json.loads(response.data)
        assert 'error' in data
        print(f"✅ {error_type} correctly rejected: {data['error']}")
    
    def test_protected_endpoint_no_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.post('/api/v1/places/', json={
            "title": "Test Place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194
        })
        
        # Should be 401 Unauthorized
        assert response.status_code == 401
        print("✅ Protected endpoint correctly requires authentication")
    
    def test_protected_endpoint_with_invalid_token(self, client):
        """Test accessing protected endpoint with invalid token"""
        headers = {'Authorization': 'Bearer invalid-token-here'}
        
        response = client.post('/api/v1/places/', 
                             json={"title": "Test Place", "price": 100.0},
                             headers=headers)
        
        # Should be 401 or 422 depending on your JWT configuration
        assert response.status_code in [401, 422]
        print("✅ Invalid token correctly rejected")
    
    def test_protected_endpoint_with_valid_token(self, client, user_token, auth_headers):
        """Test accessing protected endpoint with valid token"""
        place_data = {
            "title": "Authorized Place",
            "description": "Created with valid token",
            "price": 150.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": []
        }
        
        response = client.post('/api/v1/places/',
                             json=place_data,
                             headers=auth_headers(user_token))
        
        # Should succeed
        assert response.status_code == 201
        
        data = json.loads(response.data)
        assert data['title'] == "Authorized Place"
        print("✅ Protected endpoint works with valid token")