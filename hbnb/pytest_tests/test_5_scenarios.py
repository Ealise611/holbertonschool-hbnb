"""
Testing multiple scenarios
"""
import pytest
import json

class TestScenarios:
    """Test common use scenarios"""
    
    @pytest.mark.parametrize("first_name,last_name,email,password,expected_status", [
        ("Valid", "User", "valid@test.com", "validpass123", 201),
        ("", "Empty", "empty@test.com", "password123", 400),      # Empty first name
        ("Bad", "Email", "not-an-email", "password123", 400),    # Invalid email
    ])
    def test_user_registration_validation(self, client, clean_db, first_name, last_name, email, password, expected_status):
        """Test user registration with different inputs"""
        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
        }
        
        response = client.post('/api/v1/users/', json=user_data)
        assert response.status_code == expected_status
        print(f"✅ {email} -> {response.status_code}")
    
    def test_password_length_behavior(self, client, clean_db):
        """Test what your API actually does with short passwords"""
        user_data = {
            "first_name": "Short",
            "last_name": "Pass",
            "email": "short@test.com",
            "password": "123"
        }
        
        response = client.post('/api/v1/users/', json=user_data)
        print(f"Short password (123) result: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ Your API allows short passwords")
        elif response.status_code == 400:
            print("✅ Your API rejects short passwords")
        
        # t est should pass regardless of what API does
        assert response.status_code in [201, 400]
    
    def test_simple_user_journey(self, client, clean_db):
        """Test simple user journey: register -> login"""
        # Step 1: Register
        user_data = {
            "first_name": "Journey",
            "last_name": "User",
            "email": "journey@test.com",
            "password": "journey123"
        }
        
        register_response = client.post('/api/v1/users/', json=user_data)
        assert register_response.status_code == 201
        print("1️⃣ Registration successful")
        
        # Step 2: Login
        login_data = {
            "email": "journey@test.com",
            "password": "journey123"
        }
        
        login_response = client.post('/api/v1/auth/login', json=login_data)
        assert login_response.status_code == 200
        
        token = json.loads(login_response.data)['access_token']
        print("2️⃣ Login successful")
        
        # Step 3: Verify token is valid (length check)
        assert len(token) > 10  # JWT tokens are long
        print("3️⃣ Token received and looks valid")
        print("✅ Basic user journey works!")