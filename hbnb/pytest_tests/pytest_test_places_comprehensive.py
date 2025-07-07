"""
Comprehensive place management tests
Tests CRUD operations, ownership, relationships
"""
import pytest
import json

@pytest.mark.api
class TestPlaceCreation:
    """Test place creation functionality"""
    
    def test_create_place_success(self, client, user_token, auth_headers, sample_amenity):
        """Test successful place creation"""
        place_data = {
            "title": "Beautiful House",
            "description": "A lovely place to stay",
            "price": 150.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "amenities": [str(sample_amenity.id)]
        }
        
        response = client.post(
            '/api/v1/places/',
            json=place_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == "Beautiful House"
        assert data['price'] == 150.0
        assert 'owner_id' in data
        print(f"✅ Place created successfully: {data['id']}")
    
    @pytest.mark.parametrize("invalid_data,expected_error", [
        ({"title": "", "price": 100, "latitude": 40, "longitude": -74}, "title"),
        ({"title": "Test", "price": -50, "latitude": 40, "longitude": -74}, "price"),
        ({"title": "Test", "price": 100, "latitude": 95, "longitude": -74}, "latitude"),
        ({"title": "Test", "price": 100, "latitude": 40, "longitude": 185}, "longitude"),
    ])
    def test_place_validation_errors(self, client, user_token, auth_headers, invalid_data, expected_error):
        """Test place validation with invalid data"""
        invalid_data["amenities"] = []
        
        response = client.post(
            '/api/v1/places/',
            json=invalid_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        print(f"✅ Validation error for {expected_error}: {data['error']}")

@pytest.mark.api  
class TestPlaceOwnership:
    """Test place ownership and permissions"""
    
    def test_owner_can_update_place(self, client, user_token, auth_headers, sample_place):
        """Test that place owner can update their place"""
        update_data = {
            "title": "Updated by Owner",
            "price": 200.0
        }
        
        response = client.put(
            f'/api/v1/places/{sample_place.id}',
            json=update_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Updated by Owner"
        print("✅ Owner can update their own place")
    
    def test_non_owner_cannot_update_place(self, client, clean_db, app, user_token, auth_headers):
        """Test that non-owners cannot update places"""
        # Create another user and their place
        with app.app_context():
            from app.models.user import User
            from app.models.place import Place
            
            other_user = User(
                first_name="Other",
                last_name="User", 
                email="other@test.com"
            )
            other_user.hash_password("otherpass")
            clean_db.session.add(other_user)
            clean_db.session.commit()
            clean_db.session.refresh(other_user)
            
            other_place = Place(
                title="Other's Place",
                description="Not yours",
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner=other_user
            )
            clean_db.session.add(other_place)
            clean_db.session.commit()
            clean_db.session.refresh(other_place)
        
        # Try to update other user's place
        update_data = {"title": "Hacked Place"}
        
        response = client.put(
            f'/api/v1/places/{other_place.id}',
            json=update_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 403
        data = json.loads(response.data)
        assert data['error'] == 'Unauthorized action'
        print("✅ Non-owner correctly forbidden from updating place")
    
    def test_admin_can_update_any_place(self, client, admin_token, auth_headers, sample_place):
        """Test that admin can update any place"""
        update_data = {
            "title": "Updated by Admin",
            "description": "Admin override"
        }
        
        response = client.put(
            f'/api/v1/places/{sample_place.id}',
            json=update_data,
            headers=auth_headers(admin_token)
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == "Updated by Admin"
        print("✅ Admin can update any place")

@pytest.mark.api
class TestPlaceRetrieval:
    """Test place retrieval functionality"""
    
    def test_get_all_places_public(self, client, sample_place):
        """Test that anyone can view places list"""
        response = client.get('/api/v1/places/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        print(f"✅ Public place list retrieved: {len(data)} places")
    
    def test_get_place_with_details(self, client, sample_place):
        """Test retrieving place with full details"""
        response = client.get(f'/api/v1/places/{sample_place.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Check all expected fields are present
        required_fields = ['id', 'title', 'description', 'price', 'latitude', 'longitude', 'owner']
        for field in required_fields:
            assert field in data
            
        # Check owner details are included
        assert 'first_name' in data['owner']
        assert 'email' in data['owner']
        assert 'password' not in data['owner']  # Password should not be included
        
        print("✅ Place details retrieved with owner information")
    
    def test_get_nonexistent_place(self, client):
        """Test getting place that doesn't exist"""
        response = client.get('/api/v1/places/nonexistent-id-12345')
        assert response.status_code == 404
        print("✅ Non-existent place correctly returns 404")

# Add fixture for sample_place if not already in conftest.py
@pytest.fixture
def sample_place(clean_db, sample_user, app):
    """Create a sample place for testing"""
    with app.app_context():
        from app.models.place import Place
        
        place = Place(
            title="Test Place",
            description="A place for testing",
            price=100.0,
            latitude=40.7128,
            longitude=-74.0060,
            owner=sample_user
        )
        clean_db.session.add(place)
        clean_db.session.commit()
        clean_db.session.refresh(place)
        
        print(f"✅ Created sample place: {place.title} (ID: {place.id})")
        return place