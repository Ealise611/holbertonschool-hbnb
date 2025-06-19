# HBnB API v1 - Testing and Validation Documentation

## Table of Contents
1. [Overview](#overview)
2. [Validation Implementation](#validation-implementation)
3. [Postman API Testing](#postman-api-testing)
4. [Unit Testing Framework](#unit-testing-framework)
5. [Swagger Documentation](#swagger-documentation)
6. [Testing Summary](#testing-summary)

---

## 1. Overview

This document provides comprehensive testing and validation documentation for the HBnB API v1. The testing strategy includes:

- **Basic validation implementation** for all entity models
- **Black-box testing using Postman** collection
- **Unit testing framework** for automated testing
- **Detailed testing report** highlighting successful and failed cases

### Test Execution Summary
- **Total API Tests**: 27
- **Passed**: 27 (100%)
- **Failed**: 0 (0%)
- **Total Execution Time**: 2,082ms
- **Test Environment**: http://127.0.0.1:5000
- **Testing Tool**: Postman Collection Runner
- **Test Date**: June 19, 2025

---

## 2. Validation Implementation

Basic validation checks have been implemented for all entity models. The following validation rules are enforced:

### 2.1 User Model Validation

**Validation Rules Tested:**
- ✅ First name: Required, non-empty, max 50 characters
- ✅ Last name: Required, non-empty, max 50 characters
- ✅ Email: Required, valid format using regex validation
- ✅ Email uniqueness: Enforced at service layer
- ✅ Input cleaning: Automatic trimming of whitespace

**Test Results:**
- Empty first name → 400 "First name is required and be ≤ 50 characters"
- Name over 50 chars → 400 "First name is required and be ≤ 50 characters"
- Invalid email format → 400 "Invalid email"
- Duplicate email → 400 "Email already registered"

### 2.2 Place Model Validation

**Validation Rules Tested:**
- ✅ Title: Required, max 100 characters
- ✅ Price: Required, positive number
- ✅ Latitude: Required, between -90.0 and 90.0
- ✅ Longitude: Required, between -180.0 and 180.0
- ✅ Owner: Must reference valid User entity

**Test Results:**
- Empty title → 400 "Title is required and must be ≤ 100 characters"
- Negative price → 400 "Price must be a positive number"
- Invalid latitude (>90) → 400 "Latitude must be between -90 and 90"
- Invalid longitude (>180) → 400 "Longitude must be between -180 and 180"
- Invalid owner → 400 "Owner not found"

### 2.3 Review Model Validation

**Validation Rules Tested:**
- ✅ Text: Required, non-empty
- ✅ Rating: Required, integer between 1 and 5
- ✅ Place: Must reference valid Place entity
- ✅ User: Must reference valid User entity
- ✅ Duplicate prevention: User can only review each place once

**Test Results:**
- Empty text → 400 "Review text is required"
- Rating below 1 or above 5 → 400 "Rating must be between 1 and 5"
- Invalid rating (10) → 400 "Rating must be between 1 and 5"
- Non-existent place → 400 "Place not found"
- Duplicate review → 400 "User has already reviewed this place"

### 2.4 Amenity Model Validation

**Validation Rules Tested:**
- ✅ Name: Required, max 50 characters
- ✅ Description: Optional field with default empty string

**Test Results:**
- Empty name → 400 "Amenity name is required and be ≤ 50 characters"
- Name over 50 chars → 400 "Amenity name is required and be ≤ 50 characters"

### 2.5 Common Validation Features

**BaseModel Foundation:**
- ✅ UUID generation for unique IDs
- ✅ Automatic timestamp creation and updates
- ✅ Generic update method for all models

**Service Layer Validation:**
- ✅ Entity existence checks before creating relationships
- ✅ Email uniqueness enforcement across the system
- ✅ Business rule enforcement (e.g., duplicate review prevention)

---

## 3. Postman API Testing

### 3.1 Test Execution Summary
- **Tool**: Postman Collection "HBnB API v1"
- **Collection Description**: "API testing for HBnB Evolution Application"
- **Total Tests**: 27
- **Success Rate**: 100% (27/27 passed)
- **Total Execution Time**: 2,082ms
- **Average Response Time**: 77ms
- **Test Environment**: http://127.0.0.1:5000

### 3.2 Testing Methodology

**Testing Process:**
1. **Setup**: Created Postman collection with 27 test cases
2. **Data Preparation**: Used variables for dynamic ID management
3. **Test Execution**: Sequential execution with dependency management
4. **Validation**: Each test includes status code and response validation
5. **Edge Case Testing**: Tested boundary conditions and error scenarios

**Testing Approach:**
- Black-box methodology (testing API behaviour without internal knowledge)
- Comprehensive CRUD operation coverage
- Relationship and validation testing

### 3.3 Test Categories

| Endpoint Category | Tests | Results | Key Validations |
|------------------|-------|---------|-----------------|
| User Management | 9 | ✅ 9/9 | Email validation, uniqueness, CRUD operations |
| Place Management | 6 | ✅ 6/6 | Coordinate validation, owner relationships |
| Review Management | 6 | ✅ 6/6 | Rating validation, user-place relationships |
| Amenity Management | 6 | ✅ 6/6 | Name validation, CRUD operations |

### 3.4 Test Organisation Structure

**Collection Structure:**
1. **Create All** - Initial data setup (9 tests)
2. **Users** - User management operations (6 tests)
3. **Amenity** - Amenity operations (3 tests)
4. **Places** - Place management operations (4 tests)
5. **Reviews** - Review operations (5 tests)

**Variable Management:**
- Dynamic ID management using Postman variables ({{user1_id}}, {{amenity1_id}}, etc.)
- Sequential test execution with proper data relationships
- Automated test script validation for each endpoint

### 3.5 Key Test Scenarios

**Positive Test Cases:**
- ✅ User creation with valid data → 201 Created
- ✅ Place creation with owner and amenities → 201 Created
- ✅ Review creation with valid rating (1-5) → 201 Created
- ✅ Amenity creation with name and description → 201 Created
- ✅ Data retrieval by ID → 200 OK with complete object data
- ✅ Data updates → 200 OK with updated information
- ✅ Review deletion → 200 OK with success message

**Negative Test Cases:**
- ✅ Invalid email format → 400 "Invalid email"
- ✅ Duplicate email registration → 400 "Email already registered"
- ✅ Invalid review rating (>5) → 400 "Rating must be between 1 and 5"
- ✅ Invalid place coordinates → 400 "Latitude must be between -90 and 90"
- ✅ Non-existent resource access → 404 "User not found"
- ✅ Empty required fields → 400 with appropriate error messages

**Example Test Case**

**User Creation Validation:**
```http
POST http://127.0.0.1:5000/api/v1/users/
Content-Type: application/json

{
  "first_name": "Invalid",
  "last_name": "User",
  "email": "invalid-email"
}
```

**Response: 400 Bad Request**
```json
{
  "error": "Invalid email"
}
```

**Postman Test Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Error message present", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('error');
});
```

### 3.6 Performance Results

| Operation Type | Average Response Time | Test Count | Status |
|----------------|----------------------|------------|--------|
| POST (Create) | 75ms | 8 tests | ✅ Under 150ms |
| GET (Retrieve) | 77ms | 8 tests | ✅ Under 150ms |
| PUT (Update) | 76ms | 4 tests | ✅ Under 150ms |
| DELETE | 124ms | 1 test | ✅ Under 150ms |

### 3.7 Relationship Testing

**Successfully Tested Relationships:**
- ✅ Place-to-Owner associations with complete user data
- ✅ Place-to-Amenities many-to-many relationships
- ✅ Review-to-User and Review-to-Place associations
- ✅ Cascading data retrieval (places include owner and amenities)

### 3.8 Error Handling Validation

**HTTP Status Code Compliance:**
- ✅ 200 OK: Successful GET, PUT, DELETE operations (15 tests)
- ✅ 201 Created: Successful POST operations (8 tests)
- ✅ 400 Bad Request: Validation errors (4 tests)
- ✅ 404 Not Found: Resource not found (1 test)

**Error Response Format Consistency:**
- All error responses return JSON with descriptive error messages
- Proper error categorisation (validation vs. not found vs. server errors)
- Consistent error message formatting across all endpoints

---

## 4. Unit Testing Framework

### 4.1 Test Structure Implementation

The unit testing framework includes comprehensive test coverage:

```
tests/
├── __init__.py
├── base_test.py           # Base test class with repository cleanup
├── test_user.py          # User model and endpoint tests
├── test_amenity.py       # Amenity model and endpoint tests  
├── test_place.py         # Place model and endpoint tests
├── test_review.py        # Review model and endpoint tests
├── run_all_tests.py      # Test runner for all tests
└── how_to_run_tests.md   # Test execution instructions
```

### 4.2 Base Test Implementation (`tests/base_test.py`)

**Key Features:**
- ✅ Repository cleanup between tests
- ✅ Flask test client setup
- ✅ Proper test isolation

```python
class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.clear_repositories()
    
    def clear_repositories(self):
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()
```

### 4.3 User Testing (`tests/test_user.py`)

**Test Coverage:**
- ✅ `test_create_user_success` - Valid user creation
- ✅ `test_create_user_invalid_email` - Email validation
- ✅ `test_create_user_missing_fields` - Required field validation
- ✅ `test_create_user_duplicate_email` - Duplicate prevention
- ✅ `test_get_user_by_id` - Individual user retrieval
- ✅ `test_get_all_users` - User list retrieval
- ✅ `test_update_user` - User modification
- ✅ `test_get_nonexistent_user` - 404 handling
- ✅ `test_user_model_creation` - Direct model testing

### 4.4 Place Testing (`tests/test_place.py`)

**Test Coverage:**
- ✅ `test_create_place_success` - Valid place creation
- ✅ `test_create_place_invalid_price` - Price validation
- ✅ `test_create_place_invalid_coordinates` - Coordinate validation
- ✅ `test_create_place_invalid_owner` - Owner validation
- ✅ `test_get_all_places` - Place list retrieval
- ✅ `test_get_place_by_id` - Place with relationships
- ✅ `test_update_place` - Place modification
- ✅ `test_get_nonexistent_place` - 404 handling

### 4.5 Review Testing (`tests/test_review.py`)

**Test Coverage:**
- ✅ `test_create_review_success` - Valid review creation
- ✅ `test_create_review_invalid_rating` - Rating validation (0, 6)
- ✅ `test_create_review_missing_text` - Text requirement
- ✅ `test_create_review_invalid_user` - User validation
- ✅ `test_create_review_invalid_place` - Place validation
- ✅ `test_get_all_reviews` - Review list retrieval
- ✅ `test_get_review_by_id` - Individual review
- ✅ `test_update_review` - Review modification
- ✅ `test_delete_review` - Review deletion

### 4.6 Amenity Testing (`tests/test_amenity.py`)

**Test Coverage:**
- ✅ `test_create_amenity_success` - Valid amenity creation
- ✅ `test_create_amenity_missing_name` - Name requirement
- ✅ `test_get_all_amenities` - Amenity list retrieval
- ✅ `test_get_amenity_by_id` - Individual amenity
- ✅ `test_update_amenity` - Amenity modification
- ✅ `test_get_nonexistent_amenity` - 404 handling
- ✅ `test_amenity_model_creation` - Direct model testing

### 4.7 Running Unit Tests

**Individual Test Execution:**
```bash
cd hbnb/
python3 tests/test_user.py
python3 tests/test_amenity.py
python3 tests/test_place.py
python3 tests/test_review.py
```

**All Tests Execution:**
```bash
cd hbnb/
python3 tests/run_all_tests.py
```

**Expected Output:**
```
Test Summary:
Tests run: 32
Failures: 0
Errors: 0
Success rate: 100.0%
```

---

## 5. Swagger Documentation

### 5.1 API Documentation

The Flask-RESTx framework automatically generates Swagger documentation available at:
```
http://127.0.0.1:5000/
```

### 5.2 Features Verified

- ✅ Interactive API Explorer
- ✅ Request/Response Schemas
- ✅ Validation Rules Documentation
- ✅ Error Response Formats
- ✅ Model Definitions

### 5.3 Documented Endpoints

- ✅ Users: POST, GET (all), GET (by ID), PUT
- ✅ Places: POST, GET (all), GET (by ID), PUT
- ✅ Reviews: POST, GET (all), GET (by ID), PUT, DELETE
- ✅ Amenities: POST, GET (all), GET (by ID), PUT
