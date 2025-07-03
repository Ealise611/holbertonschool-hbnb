"""
Unit tests for Admin Review Bypass functionality
"""
import json
from tests.base_test import BaseTestCase


class TestAdminReviews(BaseTestCase):
    """Test cases for Admin Review Management"""

    def setUp(self):
        """Set up test client, users, places, and reviews"""
        super().setUp()
        
        # Create admin
        self.client.post('/api/v1/auth/create-admin')
        admin_login = self.client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.io",
            "password": "admin123"
        })
        self.admin_token = json.loads(admin_login.data)['access_token']
        
        # Create place owner
        owner_response = self.client.post('/api/v1/users/', json={
            "first_name": "Place",
            "last_name": "Owner",
            "email": "owner@test.com",
            "password": "password123"
        })
        self.owner_id = json.loads(owner_response.data)['id']
        owner_login = self.client.post('/api/v1/auth/login', json={
            "email": "owner@test.com",
            "password": "password123"
        })
        self.owner_token = json.loads(owner_login.data)['access_token']
        
        # Create reviewer
        reviewer_response = self.client.post('/api/v1/users/', json={
            "first_name": "Review",
            "last_name": "Author",
            "email": "reviewer@test.com",
            "password": "password123"
        })
        self.reviewer_id = json.loads(reviewer_response.data)['id']
        reviewer_login = self.client.post('/api/v1/auth/login', json={
            "email": "reviewer@test.com",
            "password": "password123"
        })
        self.reviewer_token = json.loads(reviewer_login.data)['access_token']
        
        # Create third user
        user3_response = self.client.post('/api/v1/users/', json={
            "first_name": "Other",
            "last_name": "User",
            "email": "other@test.com",
            "password": "password123"
        })
        self.other_id = json.loads(user3_response.data)['id']
        other_login = self.client.post('/api/v1/auth/login', json={
            "email": "other@test.com",
            "password": "password123"
        })
        self.other_token = json.loads(other_login.data)['access_token']
        
        # Create place
        place_response = self.client.post('/api/v1/places/',
                                        json={
                                            "title": "Test Place",
                                            "description": "For review testing",
                                            "price": 100.0,
                                            "latitude": 40.7128,
                                            "longitude": -74.0060,
                                            "amenities": []
                                        },
                                        headers={'Authorization': f'Bearer {self.owner_token}'})
        self.place_id = json.loads(place_response.data)['id']
        
        # Create review by reviewer
        review_response = self.client.post('/api/v1/reviews/',
                                         json={
                                             "text": "Great place!",
                                             "rating": 5,
                                             "place_id": self.place_id
                                         },
                                         headers={'Authorization': f'Bearer {self.reviewer_token}'})
        self.review_id = json.loads(review_response.data)['id']

    def test_review_author_can_update_own_review(self):
        """Test review author can update their own review"""
        update_data = {
            "text": "Updated review text",
            "rating": 4
        }
        
        response = self.client.put(f'/api/v1/reviews/{self.review_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.reviewer_token}'})
        
        self.assertEqual(response.status_code, 200)

    def test_non_author_cannot_update_review(self):
        """Test non-author cannot update review"""
        update_data = {
            "text": "Unauthorized update",
            "rating": 1
        }
        
        response = self.client.put(f'/api/v1/reviews/{self.review_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.other_token}'})
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Unauthorized action')

    def test_admin_can_update_any_review(self):
        """Test admin can update any review (bypass ownership)"""
        update_data = {
            "text": "Updated by admin",
            "rating": 3
        }
        
        response = self.client.put(f'/api/v1/reviews/{self.review_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 200)

    def test_review_author_can_delete_own_review(self):
        """Test review author can delete their own review"""
        response = self.client.delete(f'/api/v1/reviews/{self.review_id}',
                                    headers={'Authorization': f'Bearer {self.reviewer_token}'})
        
        self.assertEqual(response.status_code, 200)
        
        # Verify deletion
        get_response = self.client.get(f'/api/v1/reviews/{self.review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_non_author_cannot_delete_review(self):
        """Test non-author cannot delete review"""
        response = self.client.delete(f'/api/v1/reviews/{self.review_id}',
                                    headers={'Authorization': f'Bearer {self.other_token}'})
        
        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_any_review(self):
        """Test admin can delete any review (bypass ownership)"""
        # Create another review to delete
        review_response = self.client.post('/api/v1/reviews/',
                                         json={
                                             "text": "To be deleted by admin",
                                             "rating": 2,
                                             "place_id": self.place_id
                                         },
                                         headers={'Authorization': f'Bearer {self.reviewer_token}'})
        review_to_delete = json.loads(review_response.data)['id']
        
        response = self.client.delete(f'/api/v1/reviews/{review_to_delete}',
                                    headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 200)

    def test_users_cannot_review_own_places(self):
        """Test users cannot review their own places"""
        review_data = {
            "text": "Reviewing my own place",
            "rating": 5,
            "place_id": self.place_id
        }
        
        response = self.client.post('/api/v1/reviews/',
                                  json=review_data,
                                  headers={'Authorization': f'Bearer {self.owner_token}'})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)