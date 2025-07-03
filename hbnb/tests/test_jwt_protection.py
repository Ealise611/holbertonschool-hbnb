"""
Unit tests for JWT Token Protection on endpoints
"""
import json
from tests.base_test import BaseTestCase


class TestJWTProtection(BaseTestCase):
    """Test cases for JWT Token Protection"""

    def setUp(self):
        """Set up test client and test data"""
        super().setUp()
        
        # Create test user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test@jwt.com",
            "password": "password123"
        })
        self.user_id = json.loads(user_response.data)['id']
        
        # Get user token
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "test@jwt.com",
            "password": "password123"
        })
        self.valid_token = json.loads(login_response.data)['access_token']

    def test_protected_endpoint_without_token(self):
        """Test accessing protected endpoint without token"""
        place_data = {
            "title": "Test Place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 401)

    def test_protected_endpoint_with_invalid_token(self):
        """Test accessing protected endpoint with invalid token"""
        place_data = {
            "title": "Test Place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  headers={'Authorization': 'Bearer invalid_token'})
        self.assertEqual(response.status_code, 422)  # JWT decode error

    def test_protected_endpoint_with_valid_token(self):
        """Test accessing protected endpoint with valid token"""
        place_data = {
            "title": "Test Place",
            "description": "Valid token test",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "amenities": []
        }
        
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                  headers={'Authorization': f'Bearer {self.valid_token}'})
        self.assertEqual(response.status_code, 201)

    def test_public_endpoint_accessible_without_token(self):
        """Test public endpoints are accessible without token"""
        # Test GET users (public)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        
        # Test GET places (public)
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        
        # Test GET amenities (public)
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)

    def test_malformed_authorization_header(self):
        """Test malformed Authorization header"""
        place_data = {
            "title": "Test Place",
            "price": 100.0,
            "latitude": 40.7128,
            "longitude": -74.0060
        }
        
        # Missing 'Bearer' prefix
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  headers={'Authorization': self.valid_token})
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
