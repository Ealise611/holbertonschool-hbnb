"""
Unit tests for Amenity endpoints and model
"""
import json
from base_test import BaseTestCase
from app.models.amenity import Amenity


class TestAmenity(BaseTestCase):
    """Test cases for Amenity functionality"""

    def test_create_amenity_success(self):
        """Test successful amenity creation"""
        response = self.client.post('/api/v1/amenities/', 
                                  json={"name": "Wi-Fi"})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_create_amenity_missing_name(self):
        """Test amenity creation without name"""
        response = self.client.post('/api/v1/amenities/', 
                                  json={})
        
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        # Create some amenities first
        amenities = ["Wi-Fi", "Air Conditioning", "Pool"]
        for amenity_name in amenities:
            self.client.post('/api/v1/amenities/', 
                           json={"name": amenity_name})
        
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    def test_get_amenity_by_id(self):
        """Test retrieving amenity by ID"""
        # Create amenity
        create_response = self.client.post('/api/v1/amenities/', 
                                         json={"name": "Parking"})
        amenity_id = json.loads(create_response.data)['id']
        
        # Get amenity
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Parking')

    def test_update_amenity(self):
        """Test updating amenity"""
        # Create amenity
        create_response = self.client.post('/api/v1/amenities/', 
                                         json={"name": "Basic Wi-Fi"})
        amenity_id = json.loads(create_response.data)['id']
        
        # Update amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}',
                                 json={"name": "High-Speed Wi-Fi"})
        
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_amenity(self):
        """Test getting amenity that doesn't exist"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_amenity_model_creation(self):
        """Test Amenity model creation directly"""
        amenity = Amenity(name="Swimming Pool")
        self.assertEqual(amenity.name, "Swimming Pool")
        self.assertIsNotNone(amenity.id)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)