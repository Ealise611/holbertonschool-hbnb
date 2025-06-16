#!/usr/bin/env python3
"""Run all simple tests including BaseModel"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_all_tests():
    print("🧪 Running All Simple Model Tests...")
    print("=" * 50)
    
    try:
        # Test 0: BaseModel (foundation)
        print("\n0. Testing BaseModel:")
        from app.models.base_model import BaseModel
        base = BaseModel()
        assert hasattr(base, 'id')
        assert hasattr(base, 'created_at')
        assert hasattr(base, 'updated_at')
        
        # Test save method
        original_time = base.updated_at
        base.save()
        assert base.updated_at > original_time
        print("✅ BaseModel creation and save test passed!")
        
        # Test 1: User
        print("\n1. Testing User Model:")
        from app.models.user import User
        user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="password123")
        assert user.first_name == "John"
        assert user.is_admin is False
        assert hasattr(user, 'id')  # Inherited from BaseModel
        print("✅ User creation test passed!")
        
        # Test 2: Amenity
        print("\n2. Testing Amenity Model:")
        from app.models.amenity import Amenity
        amenity = Amenity(name="Wi-Fi")
        assert amenity.name == "Wi-Fi"
        assert hasattr(amenity, 'id')  # Inherited from BaseModel
        print("✅ Amenity creation test passed!")
        
        # Test 3: Place
        print("\n3. Testing Place Model:")
        from app.models.place import Place
        owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com", password="password123")
        place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)
        assert place.title == "Cozy Apartment"
        assert place.price == 100
        assert hasattr(place, 'id')  # Inherited from BaseModel
        print("✅ Place creation test passed!")
        
        # Test 4: Review and relationships
        print("\n4. Testing Review Model and Relationships:")
        from app.models.review import Review
        review = Review(text="Great stay!", rating=5, place=place, user=owner)
        place.add_review(review)
        
        assert len(place.reviews) == 1
        assert place.reviews[0].text == "Great stay!"
        assert review.place == place
        assert review.user == owner
        assert hasattr(review, 'id')  # Inherited from BaseModel
        print("✅ Review and relationship test passed!")
        
        # Test 5: Inheritance verification
        print("\n5. Testing BaseModel Inheritance:")
        assert isinstance(user, BaseModel)
        assert isinstance(place, BaseModel)
        assert isinstance(review, BaseModel)
        assert isinstance(amenity, BaseModel)
        print("✅ All models properly inherit from BaseModel!")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed! Task 1 models are working correctly.")
        print("✅ BaseModel provides foundation for all models")
        print("✅ All models inherit ID, timestamps, and common methods")
        print("✅ Relationships between models work correctly")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        # Show more details for debugging
        import traceback
        print("\nFull error details:")
        traceback.print_exc()

if __name__ == "__main__":
    run_all_tests()