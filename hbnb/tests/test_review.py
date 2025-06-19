"""
Unit tests for Review endpoints and model
"""
import json
from base_test import BaseTestCase
from app.models.review import Review


class TestReview(BaseTestCase):
    """Test cases for Review functionality"""

    def setUp(self):
        """Set up test client and create test data"""
        super().setUp()
        
        # Create test user
        user_response = self.client.post('/api/v1/users/', 
                                       json={
                                           "first_name": "Reviewer",
                                           "last_name": "User",
                                           "email": "reviewer@example.com"
                                       })
        self.user_id = json.loads(user_response.data)['id']
        
        # Create test place
        place_response = self.client.post('/api/v1/places/', 
                                        json={
                                            "title": "Review Test Place",
                                            "price": 80.0,
                                            "latitude": 34.0522,
                                            "longitude": -118.2437,
                                            "owner_id": self.user_id,
                                            "amenities": []
                                        })
        self.place_id = json.loads(place_response.data)['id']

    def test_create_review_success(self):
        """Test successful review creation"""
        response = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Great place to stay!",
                                      "rating": 5,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place to stay!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating(self):
        """Test review creation with invalid rating"""
        # Rating too high
        response = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Review text",
                                      "rating": 6,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
        
        self.assertEqual(response.status_code, 400)
        
        # Rating too low
        response = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Review text",
                                      "rating": 0,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_text(self):
        """Test review creation without text"""
        response = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "rating": 5,
                                      "user_id": self.user_id,
                                      "place_id": self.place_id
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Test review creation with non-existent user"""
        response = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Review text",
                                      "rating": 5,
                                      "user_id": "nonexistent-user",
                                      "place_id": self.place_id
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test review creation with non-existent place"""
        response = self.client.post('/api/v1/reviews/', 
                                  json={
                                      "text": "Review text",
                                      "rating": 5,
                                      "user_id": self.user_id,
                                      "place_id": "nonexistent-place"
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        # Create a review
        self.client.post('/api/v1/reviews/', 
                        json={
                            "text": "Test review",
                            "rating": 4,
                            "user_id": self.user_id,
                            "place_id": self.place_id
                        })
        
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_review_by_id(self):
        """Test retrieving review by ID"""
        # Create review
        create_response = self.client.post('/api/v1/reviews/', 
                                         json={
                                             "text": "Test review",
                                             "rating": 4,
                                             "user_id": self.user_id,
                                             "place_id": self.place_id
                                         })
        review_id = json.loads(create_response.data)['id']
        
        # Get review
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['text'], 'Test review')

    def test_update_review(self):
        """Test updating review"""
        # Create review
        create_response = self.client.post('/api/v1/reviews/', 
                                         json={
                                             "text": "Original review",
                                             "rating": 3,
                                             "user_id": self.user_id,
                                             "place_id": self.place_id
                                         })
        review_id = json.loads(create_response.data)['id']
        
        # Update review
        response = self.client.put(f'/api/v1/reviews/{review_id}',
                                 json={
                                     "text": "Updated review",
                                     "rating": 4
                                 })
        
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        """Test deleting review"""
        # Create review
        create_response = self.client.post('/api/v1/reviews/', 
                                         json={
                                             "text": "To be deleted",
                                             "rating": 2,
                                             "user_id": self.user_id,
                                             "place_id": self.place_id
                                         })
        review_id = json.loads(create_response.data)['id']
        
        # Delete review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
