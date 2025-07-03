"""
Unit tests for Admin User Management functionality
"""
import json
from tests.base_test import BaseTestCase


class TestAdminUsers(BaseTestCase):
    """Test cases for Admin User Management"""

    def setUp(self):
        """Set up test client and create admin"""
        super().setUp()
        
        # Create admin user
        admin_response = self.client.post('/api/v1/auth/create-admin')
        self.assertEqual(admin_response.status_code, 201)
        
        # Get admin token
        login_response = self.client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.io",
            "password": "admin123"
        })
        self.admin_token = json.loads(login_response.data)['access_token']
        
        # Create regular user
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Regular",
            "last_name": "User",
            "email": "regular@test.com",
            "password": "password123"
        })
        self.regular_user_id = json.loads(user_response.data)['id']
        
        # Get regular user token
        regular_login = self.client.post('/api/v1/auth/login', json={
            "email": "regular@test.com",
            "password": "password123"
        })
        self.regular_token = json.loads(regular_login.data)['access_token']

    def test_admin_create_user_success(self):
        """Test admin creating new user"""
        new_user_data = {
            "first_name": "Admin",
            "last_name": "Created",
            "email": "admincreated@test.com",
            "password": "password123",
            "is_admin": False
        }
        
        response = self.client.post('/api/v1/users/admin',
                                  json=new_user_data,
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'admincreated@test.com')
        self.assertFalse(data['is_admin'])

    def test_admin_create_admin_user(self):
        """Test admin creating another admin user"""
        new_admin_data = {
            "first_name": "New",
            "last_name": "Admin",
            "email": "newadmin@test.com",
            "password": "password123",
            "is_admin": True
        }
        
        response = self.client.post('/api/v1/users/admin',
                                  json=new_admin_data,
                                  headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['is_admin'])

    def test_regular_user_cannot_create_user(self):
        """Test regular user cannot access admin user creation"""
        new_user_data = {
            "first_name": "Should",
            "last_name": "Fail",
            "email": "shouldfail@test.com",
            "password": "password123"
        }
        
        response = self.client.post('/api/v1/users/admin',
                                  json=new_user_data,
                                  headers={'Authorization': f'Bearer {self.regular_token}'})
        
        self.assertEqual(response.status_code, 403)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Admin privileges required')

    def test_admin_update_any_user(self):
        """Test admin can update any user's details"""
        update_data = {
            "first_name": "Updated",
            "last_name": "ByAdmin",
            "email": "updated@test.com",
            "is_admin": True
        }
        
        response = self.client.put(f'/api/v1/users/{self.regular_user_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.admin_token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['email'], 'updated@test.com')

    def test_regular_user_cannot_modify_others(self):
        """Test regular user cannot modify other users"""
        # Create another user
        other_user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Other",
            "last_name": "User",
            "email": "other@test.com",
            "password": "password123"
        })
        other_user_id = json.loads(other_user_response.data)['id']
        
        update_data = {
            "first_name": "Hacked",
            "last_name": "User"
        }
        
        response = self.client.put(f'/api/v1/users/{other_user_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.regular_token}'})
        
        self.assertEqual(response.status_code, 403)

    def test_regular_user_can_update_own_profile(self):
        """Test regular user can update their own basic details"""
        update_data = {
            "first_name": "Updated",
            "last_name": "Self"
        }
        
        response = self.client.put(f'/api/v1/users/{self.regular_user_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.regular_token}'})
        
        self.assertEqual(response.status_code, 200)

    def test_regular_user_cannot_modify_email_password(self):
        """Test regular user cannot modify email or password"""
        update_data = {
            "email": "newemail@test.com",
            "password": "newpassword"
        }
        
        response = self.client.put(f'/api/v1/users/{self.regular_user_id}',
                                 json=update_data,
                                 headers={'Authorization': f'Bearer {self.regular_token}'})
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('cannot modify email', data['error'])


if __name__ == '__main__':
    import unittest
    unittest.main(verbosity=2)
