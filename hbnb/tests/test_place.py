"""
Unit tests for Place endpoints and model
"""
import json
from base_test import BaseTestCase
from app.models.place import Place
from app.models.user import User


class TestPlace(BaseTestCase):
    """Test cases for Place functionality"""

    def setUp(self):
        """Set up test client and create test user"""
        super().setUp()
        
        # Create a test user for place ownership
        user_response = self.client.post('/api/v1/users/', 
                                       json={
                                           "first_name": "Test",
                                           "last_name": "Owner",
                                           "email": "owner@example.com"
                                       })
        self.owner_id = json.loads(user_response.data)['id']

    def test_create_place_success(self):
        """Test successful place creation"""
        response = self.client.post('/api/v1/places/', 
                                  json={
                                      "title": "Cozy Apartment",
                                      "description": "Nice place to stay",
                                      "price": 100.0,
                                      "latitude": 37.7749,
                                      "longitude": -122.4194,
                                      "owner_id": self.owner_id,
                                      "amenities": []
                                  })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Cozy Apartment')
        self.assertEqual(data['price'], 100.0)

    def test_create_place_invalid_price(self):
        """Test place creation with negative price"""
        response = self.client.post('/api/v1/places/', 
                                  json={
                                      "title": "Invalid Place",
                                      "price": -50.0,
                                      "latitude": 37.7749,
                                      "longitude": -122.4194,
                                      "owner_id": self.owner_id,
                                      "amenities": []
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_coordinates(self):
        """Test place creation with invalid coordinates"""
        # Invalid latitude (> 90)
        response = self.client.post('/api/v1/places/', 
                                  json={
                                      "title": "Invalid Place",
                                      "price": 100.0,
                                      "latitude": 95.0,
                                      "longitude": -122.4194,
                                      "owner_id": self.owner_id,
                                      "amenities": []
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        """Test place creation with non-existent owner"""
        response = self.client.post('/api/v1/places/', 
                                  json={
                                      "title": "Orphan Place",
                                      "price": 100.0,
                                      "latitude": 37.7749,
                                      "longitude": -122.4194,
                                      "owner_id": "nonexistent-owner",
                                      "amenities": []
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        """Test retrieving all places"""
        # Create a place
        self.client.post('/api/v1/places/', 
                        json={
                            "title": "Test Place",
                            "price": 75.0,
                            "latitude": 40.7128,
                            "longitude": -74.0060,
                            "owner_id": self.owner_id,
                            "amenities": []
                        })
        
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_place_by_id(self):
        """Test retrieving place by ID with owner and amenities"""
        # Create place
        create_response = self.client.post('/api/v1/places/', 
                                         json={
                                             "title": "Test Place",
                                             "price": 75.0,
                                             "latitude": 40.7128,
                                             "longitude": -74.0060,
                                             "owner_id": self.owner_id,
                                             "amenities": []
                                         })
        place_id = json.loads(create_response.data)['id']
        
        # Get place
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], place_id)
        self.assertIn('owner', data)
        self.assertIn('amenities', data)

    def test_update_place(self):
        """Test updating place information"""
        # Create place
        create_response = self.client.post('/api/v1/places/', 
                                         json={
                                             "title": "Original Title",
                                             "price": 100.0,
                                             "latitude": 37.7749,
                                             "longitude": -122.4194,
                                             "owner_id": self.owner_id,
                                             "amenities": []
                                         })
        place_id = json.loads(create_response.data)['id']
        
        # Update place
        response = self.client.put(f'/api/v1/places/{place_id}',
                                 json={
                                     "title": "Updated Title",
                                     "price": 150.0
                                 })
        
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_place(self):
        """Test getting place that doesn't exist"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)