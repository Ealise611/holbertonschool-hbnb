"""
Comprehensive review system tests
Tests business rules, relationships, and edge cases
"""
import pytest
import json

@pytest.mark.api
class TestReviewCreation:
    """Test review creation with business rules"""
    
    def test_create_review_success(self, client, clean_db, app, user_token, auth_headers):
        """Test successful review creation"""
        # Create another user and their place to review
        with app.app_context():
            from app.models.user import User
            from app.models.place import Place
            
            place_owner = User(
                first_name="Place",
                last_name="Owner",
                email="placeowner@test.com"
            )
            place_owner.hash_password("ownerpass")
            clean_db.session.add(place_owner)
            clean_db.session.commit()
            clean_db.session.refresh(place_owner)
            
            place = Place(
                title="Reviewable Place",
                description="Can be reviewed",
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner=place_owner
            )
            clean_db.session.add(place)
            clean_db.session.commit()
            clean_db.session.refresh(place)
        
        review_data = {
            "text": "Great place to stay!",
            "rating": 5,
            "place_id": str(place.id)
        }
        
        response = client.post(
            '/api/v1/reviews/',
            json=review_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['text'] == "Great place to stay!"
        assert data['rating'] == 5
        print(f"✅ Review created successfully: {data['id']}")
    
    def test_cannot_review_own_place(self, client, user_token, auth_headers, sample_place):
        """Test that users cannot review their own places"""
        review_data = {
            "text": "Reviewing my own place",
            "rating": 5,
            "place_id": str(sample_place.id)
        }
        
        response = client.post(
            '/api/v1/reviews/',
            json=review_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'cannot review your own place' in data['error'].lower()
        print("✅ Users correctly forbidden from reviewing own places")
    
    @pytest.mark.parametrize("rating,expected_status", [
        (1, 201),   # Valid
        (3, 201),   # Valid
        (5, 201),   # Valid
        (0, 400),   # Invalid - too low
        (6, 400),   # Invalid - too high
        (-1, 400),  # Invalid - negative
    ])
    def test_review_rating_validation(self, client, clean_db, app, user_token, auth_headers, rating, expected_status):
        """Test review rating validation"""
        # Create place by another user for each test
        with app.app_context():
            from app.models.user import User
            from app.models.place import Place
            
            place_owner = User(
                first_name="Rating",
                last_name="Test",
                email=f"rating{rating}@test.com"  # Unique email for each test
            )
            place_owner.hash_password("testpass")
            clean_db.session.add(place_owner)
            clean_db.session.commit()
            clean_db.session.refresh(place_owner)
            
            place = Place(
                title=f"Rating Test Place {rating}",
                description="For rating tests",
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner=place_owner
            )
            clean_db.session.add(place)
            clean_db.session.commit()
            clean_db.session.refresh(place)
        
        review_data = {
            "text": f"Rating test with {rating}",
            "rating": rating,
            "place_id": str(place.id)
        }
        
        response = client.post(
            '/api/v1/reviews/',
            json=review_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == expected_status
        print(f"✅ Rating {rating}: Expected {expected_status}, got {response.status_code}")

@pytest.mark.api
class TestReviewOwnership:
    """Test review ownership and permissions"""
    
    def test_author_can_update_review(self, client, clean_db, app, user_token, auth_headers):
        """Test that review author can update their review"""
        # Setup: Create place and review
        with app.app_context():
            from app.models.user import User, Place, Review
            
            # Get the user from token (sample_user)
            user = clean_db.session.query(User).filter_by(email="pytest.user@mysql.test").first()
            
            # Create place owner
            place_owner = User(
                first_name="Place",
                last_name="Owner",
                email="updateowner@test.com"
            )
            place_owner.hash_password("ownerpass")
            clean_db.session.add(place_owner)
            clean_db.session.commit()
            clean_db.session.refresh(place_owner)
            
            # Create place
            place = Place(
                title="Update Test Place",
                description="For update tests",
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner=place_owner
            )
            clean_db.session.add(place)
            clean_db.session.commit()
            clean_db.session.refresh(place)
            
            # Create review
            review = Review(
                text="Original review text",
                rating=3,
                place=place,
                user=user
            )
            clean_db.session.add(review)
            clean_db.session.commit()
            clean_db.session.refresh(review)
        
        # Update the review
        update_data = {
            "text": "Updated review text",
            "rating": 4
        }
        
        response = client.put(
            f'/api/v1/reviews/{review.id}',
            json=update_data,
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 200
        print("✅ Author can update their own review")
    
    def test_author_can_delete_review(self, client, clean_db, app, user_token, auth_headers):
        """Test that review author can delete their review"""
        # Setup similar to update test
        with app.app_context():
            from app.models.user import User, Place, Review
            
            user = clean_db.session.query(User).filter_by(email="pytest.user@mysql.test").first()
            
            place_owner = User(
                first_name="Delete",
                last_name="Owner",
                email="deleteowner@test.com"
            )
            place_owner.hash_password("ownerpass")
            clean_db.session.add(place_owner)
            clean_db.session.commit()
            clean_db.session.refresh(place_owner)
            
            place = Place(
                title="Delete Test Place",
                description="For delete tests",
                price=100.0,
                latitude=40.0,
                longitude=-74.0,
                owner=place_owner
            )
            clean_db.session.add(place)
            clean_db.session.commit()
            clean_db.session.refresh(place)
            
            review = Review(
                text="Review to delete",
                rating=2,
                place=place,
                user=user
            )
            clean_db.session.add(review)
            clean_db.session.commit()
            clean_db.session.refresh(review)
        
        # Delete the review
        response = client.delete(
            f'/api/v1/reviews/{review.id}',
            headers=auth_headers(user_token)
        )
        
        assert response.status_code == 200
        
        # Verify deletion
        get_response = client.get(f'/api/v1/reviews/{review.id}')
        assert get_response.status_code == 404
        print("✅ Author can delete their own review")
Running the New Test Suite
bash