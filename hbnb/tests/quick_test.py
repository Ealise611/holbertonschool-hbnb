#!/usr/bin/env python3
"""Quick test for immediate debugging"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def quick_test():
    print("🚀 Quick Model Test - Step by Step")
    
    # Step 1: Test imports
    print("\n1. Testing imports...")
    try:
        from app.models.user import User
        print("✅ User imported")
        from app.models.place import Place
        print("✅ Place imported")
        from app.models.amenity import Amenity
        print("✅ Amenity imported")
        from app.models.review import Review
        print("✅ Review imported")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return
    
    # Step 2: Test User creation
    print("\n2. Testing User creation...")
    try:
        user = User("John", "Doe", "john@example.com", "password123")
        print(f"✅ User created: {user.first_name}")
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        return
    
    # Step 3: Test Place creation
    print("\n3. Testing Place creation...")
    try:
        place = Place("Test House", "Nice place", 100.0, 40.7, -74.0, user)
        print(f"✅ Place created: {place.title}")
    except Exception as e:
        print(f"❌ Place creation failed: {e}")
        return
    
    print("\n🎉 Quick test passed! Your models are working.")

if __name__ == "__main__":
    quick_test()