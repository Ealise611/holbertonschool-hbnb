"""
Unit tests for Authentication endpoints and JWT functionality
"""
import json
from tests.base_test import BaseTestCase


class TestAuth(BaseTestCase):
    """Test cases for Authentication functionality"""

    def setUp(self):
        """Set up test client and create test users"""
        super().setUp()
        
        # Create a regular user
        self.regular_user_data = {
            "first_name": "Regular",
            "last_name": "User",
            "email": "regular@test.com",
            "password": "password123"
        }
        user_response = self.client.post('/api/v1/users/', json=self.regular_user_data)
        self.regular_user_id = json.loads(user_response.data)['id']
        
        # Create admin user
        admin_response = self.client.post('/api/v1/auth/create-admin')
        self.assertEqual(admin_response.status_code, 201)

    def test_create_admin_success(self):
        """Test admin user creation endpoint"""
        # Clear existing admin
        self.clear_repositories()
        
        response = self.client.post('/api/v1/auth/create-admin')
        self.assertEqual(response.status_code, 201)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(data['email'], 'admin@hbnb.io')

    def test_create_admin_duplicate(self):
        """Test creating admin when one already exists"""
        response = self.client.post('/api/v1/auth/create-admin')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Admin already exists')

    def test_login_success_regular_user(self):
        """Test successful login with regular user"""
        login_data = {
            "email": "regular@test.com",
            "password": "password123"
        }
        
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_login_success_admin_user(self):
        """Test successful login with admin user"""
        login_data = {
            "email": "admin@hbnb.io",
            "password": "admin123"
        }
        
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        login_data = {
            "email": "regular@test.com",
            "password": "wrongpassword"
        }
        
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 401)
        
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid credentials')

    def test_login_nonexistent_user(self):
        """Test login with non-existent user"""
        login_data = {
            "email": "nonexistent@test.com",
            "password": "password123"
        }
        
        response = self.client.post('/api/v1/auth/login', json=login_data)
        self.assertEqual(response.status_code, 401)

    def get_admin_token(self):
        """Helper method to get admin JWT token"""
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.io",
            "password": "admin123"
        })
        return json.loads(login_response.data)['access_token']

    def get_regular_token(self):
        """Helper method to get regular user JWT token"""
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "regular@test.com",
            "password": "password123"
        })
        return json.loads(login_response.data)['access_token']


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)