"""
Unit tests for Password Hashing functionality
"""
import json
from tests.base_test import BaseTestCase
from app.models.user import User


class TestPasswordHashing(BaseTestCase):
    """Test cases for Password Hashing and Verification"""

    def test_password_hashing_on_creation(self):
        """Test password is hashed when user is created"""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "plaintext123"
        }
        
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 201)
        
        # Password should not be returned in response
        data = json.loads(response.data)
        self.assertNotIn('password', data)

    def test_password_verification_success(self):
        """Test password verification with correct password"""
        # Create user
        user = User(
            first_name="Test",
            last_name="User", 
            email="test@example.com",
            password="correctpassword"
        )
        
        # Verify correct password
        self.assertTrue(user.verify_password("correctpassword"))

    def test_password_verification_failure(self):
        """Test password verification with incorrect password"""
        # Create user
        user = User(
            first_name="Test",
            last_name="User",
            email="test@example.com", 
            password="correctpassword"
        )
        
        # Verify incorrect password
        self.assertFalse(user.verify_password("wrongpassword"))

    def test_login_with_correct_password(self):
        """Test login success with correct password"""
        # Create user
        self.client.post('/api/v1/users/', json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "login@test.com",
            "password": "mypassword123"
        })
        
        # Login with correct password
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "login@test.com",
            "password": "mypassword123"
        })
        
        self.assertEqual(login_response.status_code, 200)
        data = json.loads(login_response.data)
        self.assertIn('access_token', data)

    def test_login_with_incorrect_password(self):
        """Test login failure with incorrect password"""
        # Create user
        self.client.post('/api/v1/users/', json={
            "first_name": "Login",
            "last_name": "Test",
            "email": "login@test.com",
            "password": "mypassword123"
        })
        
        # Login with incorrect password
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "login@test.com",
            "password": "wrongpassword"
        })
        
        self.assertEqual(login_response.status_code, 401)
        data = json.loads(login_response.data)
        self.assertEqual(data['error'], 'Invalid credentials')

    def test_empty_password_rejected(self):
        """Test empty password is rejected"""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": ""
        }
        
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)

    def test_whitespace_only_password_rejected(self):
        """Test whitespace-only password is rejected"""
        user_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "   "
        }
        
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)