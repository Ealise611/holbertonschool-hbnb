"""
Testing authentication
"""
import pytest
import json

class TestUserAPI:
    """Test User API endpoints"""
    
    def test_register_user(self, client, clean_db):
        """Test user registration endpoint"""
        # Prepare user data
        user_data = {
            "first_name": "API",
            "last_name": "Test",
            "email": "api@test.com", 
            "password": "apitest123"
        }
        
        # Make POST request to register user
        response = client.post('/api/v1/users/', json=user_data)
        
        # Check response
        assert response.status_code == 201  # 201 = Created
        
        # Parse response data
        data = json.loads(response.data)
        assert data['first_name'] == "API"
        assert data['email'] == "api@test.com"
        assert 'password' not in data  # Password should not be returned
        print("✅ User registration works!")
    
    def test_register_duplicate_email(self, client, clean_db):
        """Test that duplicate emails are rejected"""
        user_data = {
            "first_name": "First",
            "last_name": "User",
            "email": "duplicate@test.com",
            "password": "password123"
        }
        
        # First registration should work
        response1 = client.post('/api/v1/users/', json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        response2 = client.post('/api/v1/users/', json=user_data)
        assert response2.status_code == 400 
        print("✅ Duplicate email prevention works!")
    
    def test_login_user(self, client, clean_db):
        """Test user login"""
        # First register a user
        user_data = {
            "first_name": "Login",
            "last_name": "Test",
            "email": "login@test.com",
            "password": "logintest123"
        }
        client.post('/api/v1/users/', json=user_data)
        
        # Now try to login
        login_data = {
            "email": "login@test.com",
            "password": "logintest123"
        }
        
        response = client.post('/api/v1/auth/login', json=login_data)
        
        # Check login worked
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
        print("✅ User login works!")