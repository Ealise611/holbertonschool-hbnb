"""
Unit tests for User endpoints and model
"""
import json
from base_test import BaseTestCase
from app.models.user import User


class TestUser(BaseTestCase):
    """Test cases for User functionality"""

    def test_create_user_success(self):
        """Test successful user creation via API"""
        response = self.client.post('/api/v1/users/', 
                                  json={
                                      "first_name": "John",
                                      "last_name": "Doe",
                                      "email": "john.doe@example.com"
                                  })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')

    def test_create_user_invalid_email(self):
        """Test user creation with invalid email"""
        response = self.client.post('/api/v1/users/', 
                                  json={
                                      "first_name": "John",
                                      "last_name": "Doe",
                                      "email": "invalid-email"
                                  })
        
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_fields(self):
        """Test user creation with missing required fields"""
        response = self.client.post('/api/v1/users/', 
                                  json={"first_name": "John"})
        
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        """Test user creation with duplicate email"""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "duplicate@example.com"
        }
        
        # Create first user
        response1 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response1.status_code, 201)
        
        # Try to create second user with same email
        response2 = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response2.status_code, 400)

    def test_get_user_by_id(self):
        """Test retrieving user by ID"""
        # Create user first
        create_response = self.client.post('/api/v1/users/', 
                                         json={
                                             "first_name": "Jane",
                                             "last_name": "Smith",
                                             "email": "jane@example.com"
                                         })
        user_id = json.loads(create_response.data)['id']
        
        # Get user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['id'], user_id)
        self.assertEqual(data['email'], 'jane@example.com')

    def test_get_all_users(self):
        """Test retrieving all users"""
        # Create some users
        users = [
            {"first_name": "User1", "last_name": "Test", "email": "user1@example.com"},
            {"first_name": "User2", "last_name": "Test", "email": "user2@example.com"}
        ]
        
        for user_data in users:
            self.client.post('/api/v1/users/', json=user_data)
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_update_user(self):
        """Test updating user information"""
        # Create user
        create_response = self.client.post('/api/v1/users/', 
                                         json={
                                             "first_name": "Bob",
                                             "last_name": "Johnson",
                                             "email": "bob@example.com"
                                         })
        
        self.assertEqual(create_response.status_code, 201)
        user_id = json.loads(create_response.data)['id']
        
        # Update user
        response = self.client.put(f'/api/v1/users/{user_id}',
                                 json={
                                     "first_name": "Robert",
                                     "last_name": "Johnson",
                                     "email": "robert@example.com"
                                 })
        
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_user(self):
        """Test getting user that doesn't exist"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_user_model_creation(self):
        """Test User model creation directly"""
        user = User(first_name="Test", last_name="User", email="test@example.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_admin)


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)