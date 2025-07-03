"""
Unit tests for Admin Amenity Management functionality
"""
import json
from tests.base_test import BaseTestCase


class TestAdminAmenities(BaseTestCase):
    """Test cases for Admin Amenity Management"""

    def setUp(self):
        """Set up test client and tokens"""
        super().setUp()
        
        # Create admin user and get token
        self.client.post('/api/v1/auth/create-admin')
        admin_login = self.client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.io",
            "password": "admin123"
        })
        self.admin_token = json.loads(admin_login.data)['access_token']
        
        # Create regular user and get token
        self.client.post('/api/v1/users/', json={
            "first_name": "Regular",
            "last_name": "User",
            "email": "regular@test.com",
            "password": "password123"
        })
        regular_login = self.client.post('/api/v1/auth/login', json={
            "email": "regular@test.com",
            "password": "password123"
        })
        self.regular_token = json.loads(regular_login.data)['access_token']

    def test_admin_create_amenity_success(self):
        """Test admin can create amenities"""
        amenity_data = {
            "name": "Swimming Pool",
            "description": "Large outdoor pool"
        }
        
        response = self.client.post('/api/v1/amenities/',
                                  json=amenity_data,
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Swimming Pool')

    def test_regular_user_cannot_create_amenity(self):
        """Test regular user cannot create amenities"""
        amenity_data = {
            "name": "Unauthorized Amenity",
            "description": "Should not be created"
        }
        
        response = self.client.post('/api/v1/amenities/',
                                  json=amenity_data,
                                  headers={'Authorization': f'Bearer {self.regular_token}'})
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Admin privileges required')

    def test_unauthenticated_cannot_create_amenity(self):
        """Test unauthenticated user cannot create amenities"""
        amenity_data = {
            "name": "Unauthorized Amenity",
            "description": "Should not be created"
        }
        
        response = self.client.post('/api/v1/amenities/', json=amenity_data)
        self.assertEqual(response.status_code, 401)

    def test_admin_update_amenity_success(self):
        """Test admin can update amenities"""
        # Create amenity first
        amenity_response = self.client.post('/api/v1/amenities/',
                                          json={"name": "Basic Pool"},
                                          headers={'Authorization': f'Bearer {self.admin_token}'})
        amenity_id = json.loads(amenity_response.data)['id']
        
        # Update amenity
        update_data = {
            "name": "Luxury Pool",
            "description": "Premium swimming facility"
        }
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Luxury Pool')

    def test_regular_user_cannot_update_amenity(self):
        """Test regular user cannot update amenities"""
        # Create amenity as admin
        amenity_response = self.client.post('/api/v1/amenities/',
                                          json={"name": "Pool"},
                                          headers={'Authorization': f'Bearer {self.admin_token}'})
        amenity_id = json.loads(amenity_response.data)['id']
        
        # Try to update as regular user
        update_data = {"name": "Hacked Pool"}
        
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.regular_token}'})
        
        self.assertEqual(response.status_code, 403)

    def test_duplicate_amenity_name_rejected(self):
        """Test duplicate amenity names are rejected"""
        # Create first amenity
        self.client.post('/api/v1/amenities/',
                        json={"name": "Wi-Fi"},
                        headers={'Authorization': f'Bearer {self.admin_token}'})
        
        # Try to create duplicate
        response = self.client.post('/api/v1/amenities/',
                                  json={"name": "Wi-Fi"},
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Amenity already exists')

    def test_public_can_view_amenities(self):
        """Test public users can view amenities"""
        # Create amenity as admin
        self.client.post('/api/v1/amenities/',
                        json={"name": "Public Amenity"},
                        headers={'Authorization': f'Bearer {self.admin_token}'})
        
        # View as public (no token)
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
