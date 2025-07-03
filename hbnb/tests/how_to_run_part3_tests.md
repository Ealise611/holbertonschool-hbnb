"""
# How to Run Part 3 Tests

## Overview
These tests cover all new authentication and admin functionality added in Part 3:

- **test_auth.py**: Authentication endpoints (login, create admin)
- **test_admin_users.py**: Admin user management functionality  
- **test_admin_amenities.py**: Admin-only amenity creation/modification
- **test_admin_places.py**: Admin bypass for place ownership restrictions
- **test_admin_reviews.py**: Admin bypass for review ownership restrictions
- **test_password_hashing.py**: Password security and hashing
- **test_jwt_protection.py**: JWT token protection on endpoints

## Run Individual Test Files

```bash
cd hbnb/
python3 tests/test_auth.py
python3 tests/test_admin_users.py
python3 tests/test_admin_amenities.py
python3 tests/test_admin_places.py
python3 tests/test_admin_reviews.py
python3 tests/test_password_hashing.py
python3 tests/test_jwt_protection.py
```

## Run All Part 3 Tests

```bash
cd hbnb/
python3 tests/run_part3_tests.py
```

## Run All Tests (Part 2 + Part 3)

```bash
cd hbnb/
python3 tests/run_all_tests.py
```

## Expected Test Coverage

### Authentication Tests (test_auth.py)
- ✅ Admin user creation endpoint
- ✅ Duplicate admin prevention  
- ✅ User login success/failure
- ✅ JWT token generation
- ✅ Invalid credentials handling

### Admin User Management (test_admin_users.py)
- ✅ Admin can create users with admin privileges
- ✅ Regular users cannot access admin endpoints
- ✅ Admin can modify any user's details
- ✅ Regular users can only modify their own basic details
- ✅ Email/password modification restrictions

### Admin Amenity Management (test_admin_amenities.py)  
- ✅ Only admins can create/modify amenities
- ✅ Regular users get 403 Forbidden
- ✅ Public users can view amenities
- ✅ Duplicate amenity name prevention

### Admin Place Management (test_admin_places.py)
- ✅ Place owners can modify their own places
- ✅ Non-owners cannot modify places  
- ✅ Admins can modify any place (ownership bypass)
- ✅ Public users can view places

### Admin Review Management (test_admin_reviews.py)
- ✅ Review authors can modify their own reviews
- ✅ Non-authors cannot modify reviews
- ✅ Admins can modify/delete any review (ownership bypass)
- ✅ Users cannot review their own places
- ✅ Users cannot review same place twice

### Password Security (test_password_hashing.py)
- ✅ Passwords are hashed on creation
- ✅ Password verification works correctly
- ✅ Passwords not returned in API responses
- ✅ Empty/whitespace passwords rejected

### JWT Protection (test_jwt_protection.py)
- ✅ Protected endpoints require valid JWT
- ✅ Invalid/missing tokens rejected
- ✅ Public endpoints accessible without tokens
- ✅ Malformed authorization headers handled

## Test Success Criteria

All tests should pass with:
- **0 Failures**
- **0 Errors** 
- **100% Success Rate**

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure you're running from the `hbnb/` directory
2. **Token Errors**: Check JWT_SECRET_KEY is set in config
3. **Repository Errors**: Ensure repositories are cleared between tests
4. **Authentication Errors**: Verify bcrypt is properly initialized

### Debug Individual Tests:

```bash
# Run with maximum verbosity
python3 tests/test_auth.py -v

# Run specific test method
python3 -m unittest tests.test_auth.TestAuth.test_login_success_admin_user -v
```
"""
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