"""
Debug test for protected endpoints
"""
import pytest
import json

@pytest.mark.auth
class TestProtectedEndpointDebug:
    """Debug protected endpoint behavior"""
    
    def test_debug_protected_endpoint_no_token(self, client):
        """Test what happens when accessing protected endpoint without token"""
        print("\n🔍 Testing protected endpoint without token...")
        
        response = client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "Test description", 
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": []
        })
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.data.decode()}")
        print(f"Response Headers: {dict(response.headers)}")
        
        # Let's see what status code it actually returns
        # Common possibilities: 401, 403, 422
        assert response.status_code in [401, 403, 422]
        print("✅ Protected endpoint correctly requires authentication")
    
    def test_debug_protected_endpoint_with_token(self, client, user_token, auth_headers):
        """Test what happens with a valid token"""
        print("\n🔍 Testing protected endpoint WITH valid token...")
        
        place_data = {
            "title": "Authorized Test Place",
            "description": "Created with valid JWT token",
            "price": 150.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": []
        }
        
        headers = auth_headers(user_token)
        print(f"Using headers: {headers}")
        
        response = client.post('/api/v1/places/',
                             json=place_data,
                             headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.data.decode()}")
        
        if response.status_code == 201:
            data = json.loads(response.data)
            print(f"✅ Place created successfully: {data.get('id', 'No ID returned')}")
        elif response.status_code in [400, 422]:
            print("❌ Validation error - check required fields")
        elif response.status_code in [401, 403]:
            print("❌ Authentication/Authorization error")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    
    def test_debug_token_format(self, user_token, auth_headers):
        """Debug the token format"""
        print(f"\n🔍 Token starts with: {user_token[:20]}...")
        print(f"Token length: {len(user_token)}")
        
        headers = auth_headers(user_token)
        print(f"Authorization header: {headers['Authorization'][:30]}...")
        
        assert user_token is not None
        assert len(user_token) > 20  # JWT tokens are long
        assert headers['Authorization'].startswith('Bearer ')
        print("✅ Token format looks correct")
    
    def test_debug_user_fixture(self, sample_user):
        """Debug the user fixture"""
        print(f"\n🔍 Sample user details:")
        print(f"ID: {sample_user.id}")
        print(f"Email: {sample_user.email}")
        print(f"Is Admin: {sample_user.is_admin}")
        print(f"Password hash exists: {len(sample_user.password) > 10}")
        
        assert sample_user.email == "pytest.user@mysql.test"
        assert sample_user.is_admin is False
        print("✅ Sample user fixture working correctly")

@pytest.mark.auth  
class TestSimpleAuth:
    """Simple auth tests that should definitely work"""
    
    def test_login_success_simple(self, client, sample_user):
        """Simple successful login test"""
        response = client.post('/api/v1/auth/login', json={
            "email": "pytest.user@mysql.test",
            "password": "pytestpass123"
        })
        
        print(f"\nLogin response status: {response.status_code}")
        print(f"Login response body: {response.data.decode()}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        print("✅ Simple login test passed")
    
    def test_login_failure_simple(self, client, sample_user):
        """Simple login failure test"""
        response = client.post('/api/v1/auth/login', json={
            "email": "pytest.user@mysql.test",
            "password": "wrongpassword"
        })
        
        print(f"\nFailed login status: {response.status_code}")
        print(f"Failed login body: {response.data.decode()}")
        
        # Your API probably returns 401 for auth failures
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data
        print("✅ Simple login failure test passed")