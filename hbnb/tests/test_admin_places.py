"""
Unit tests for Admin Place Bypass functionality
"""
import json
from tests.base_test import BaseTestCase


class TestAdminPlaces(BaseTestCase):
    """Test cases for Admin Place Management"""

    def setUp(self):
        """Set up test client, users, and places"""
        super().setUp()
        
        # Create admin
        self.client.post('/api/v1/auth/create-admin')
        admin_login = self.client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.io",
            "password": "admin123"
        })
        self.admin_token = json.loads(admin_login.data)['access_token']
        
        # Create first user
        user1_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "One",
            "email": "owner1@test.com",
            "password": "password123"
        })
        self.user1_id = json.loads(user1_response.data)['id']
        user1_login = self.client.post('/api/v1/auth/login', json={
            "email": "owner1@test.com",
            "password": "password123"
        })
        self.user1_token = json.loads(user1_login.data)['access_token']
        
        # Create second user
        user2_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "Two",
            "email": "owner2@test.com",
            "password": "password123"
        })
        self.user2_id = json.loads(user2_response.data)['id']
        user2_login = self.client.post('/api/v1/auth/login', json={
            "email": "owner2@test.com",
            "password": "password123"
        })
        self.user2_token = json.loads(user2_login.data)['access_token']
        
        # Create place owned by user1
        place_response = self.client.post('/api/v1/places/',
                                        json={
                                            "title": "User1's Place",
                                            "description": "Test place",
                                            "price": 100.0,
                                            "latitude": 40.7128,
                                            "longitude": -74.0060,
                                            "amenities": []
                                        },
                                        headers={'Authorization': f'Bearer {self.user1_token}'})
        self.place_id = json.loads(place_response.data)['id']

    def test_owner_can_update_own_place(self):
        """Test place owner can update their own place"""
        update_data = {
            "title": "Updated by Owner",
            "price": 150.0
        }
        
        response = self.client.put(f'/api/v1/places/{self.place_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.user1_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated by Owner')

    def test_non_owner_cannot_update_place(self):
        """Test non-owner cannot update place"""
        update_data = {
            "title": "Unauthorized Update"
        }
        
        response = self.client.put(f'/api/v1/places/{self.place_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.user2_token}'})
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Unauthorized action')

    def test_admin_can_update_any_place(self):
        """Test admin can update any place (bypass ownership)"""
        update_data = {
            "title": "Updated by Admin",
            "price": 200.0
        }
        
        response = self.client.put(f'/api/v1/places/{self.place_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated by Admin')

    def test_unauthenticated_cannot_update_place(self):
        """Test unauthenticated user cannot update places"""
        update_data = {"title": "Should Fail"}
        
        response = self.client.put(f'/api/v1/places/{self.place_id}', json=update_data)
        self.assertEqual(response.status_code, 401)

    def test_authenticated_users_can_create_places(self):
        """Test any authenticated user can create places"""
        place_data = {
            "title": "New User Place",
            "description": "Created by user2",
            "price": 80.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "amenities": []
        }
        
        response = self.client.post('/api/v1/places/',
                                  json=place_data,
                                  headers={'Authorization': f'Bearer {self.user2_token}'})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['owner_id'], self.user2_id)

    def test_public_can_view_places(self):
        """Test public users can view places"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)