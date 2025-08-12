"""
Testing the User model
"""
import pytest
from app.models.user import User

class TestUserModel:
    """Test User model basics"""
    
    def test_create_user(self, app, clean_db):
        """Test creating a user"""
        with app.app_context():
            # Create a user
            user = User(
                first_name="Test",
                last_name="User", 
                email="test@example.com",
                password="password123"
            )
            
            # Save to database
            clean_db.session.add(user)
            clean_db.session.commit()
            
            # Check it worked
            assert user.id is not None
            assert user.first_name == "Test"
            assert user.email == "test@example.com"
            print(f"✅ User created with ID: {user.id}")
    
    def test_password_hashing(self, app):
        """Test that passwords get hashed"""
        with app.app_context():
            user = User(
                first_name="Password",
                last_name="Test",
                email="password@test.com",
                password="secret123"
            )
            
            # Password should be hashed, not plain text so we user not
            assert user.password != "secret123"
            
            # But we should be able to verify it
            assert user.verify_password("secret123") == True
            assert user.verify_password("wrong") == False
            print("✅ Password hashing works!")
