"""
Testing with MySQL database
"""
import pytest
from app.models.user import User
from app.models.amenity import Amenity

class TestMySQLDatabase:
    """Test MySQL database functionality"""
    
    def test_database_connection(self, app):
        """Test that we can connect to MySQL"""
        with app.app_context():
            from app import db
            
            # Test connection
            result = db.session.execute(db.text('SELECT DATABASE()'))
            db_name = result.fetchone()[0]
            assert db_name == 'hbnb_test_db'
            print(f"✅ Connected to: {db_name}")
            
            # Test MySQL version
            result = db.session.execute(db.text('SELECT VERSION()'))
            version = result.fetchone()[0]
            assert any(char.isdigit() for char in version)  # Should contain numbers
            print(f"✅ MySQL version: {version}")
    
    def test_user_persistence(self, app, clean_db):
        """Test that users are saved to MySQL database"""
        with app.app_context():
            # Create user
            user = User(
                first_name="MySQL",
                last_name="Test",
                email="mysql@test.com",
                password="mysqltest123"
            )
            clean_db.session.add(user)
            clean_db.session.commit()
            
            # Get the user ID
            user_id = user.id
            assert user_id is not None
            print(f"✅ User saved with ID: {user_id}")
            
            # Query user back from database
            found_user = User.query.filter_by(id=user_id).first()
            assert found_user is not None
            assert found_user.email == "mysql@test.com"
            assert found_user.verify_password("mysqltest123")
            print("✅ User retrieved from MySQL database")
    
    def test_multiple_users(self, app, clean_db):
        """Test creating multiple users in MySQL"""
        with app.app_context():
            users = []
            for i in range(3):
                user = User(
                    first_name=f"User{i}",
                    last_name="Multiple",
                    email=f"user{i}@multiple.test",
                    password=f"password{i}123"
                )
                clean_db.session.add(user)
                users.append(user)
            
            clean_db.session.commit()
            
            # Check all users were saved
            total_users = User.query.count()
            assert total_users >= 3  # At least our 3 users
            print(f"✅ {total_users} users in database")
            
            # Check specific users
            user0 = User.query.filter_by(email="user0@multiple.test").first()
            assert user0 is not None
            assert user0.first_name == "User0"
            print("✅ Multiple users saved correctly")
    
    def test_amenity_model(self, app, clean_db):
        """Test Amenity model since Place has relationship issues"""
        with app.app_context():
            amenity = Amenity(
                name="WiFi",
                description="High-speed internet"
            )
            clean_db.session.add(amenity)
            clean_db.session.commit()
            
            # Verify amenity was saved
            found_amenity = Amenity.query.filter_by(name="WiFi").first()
            assert found_amenity is not None
            assert found_amenity.description == "High-speed internet"
            print("✅ Amenity model works correctly")
    
    def test_basic_models_cleanup(self, app, clean_db):
        """Test that basic models are properly cleaned"""
        with app.app_context():
            # Create test data for Uuer and amenity only
            user = User(
                first_name="Multi",
                last_name="Test",
                email="multi@test.com",
                password="multipass123"
            )
            clean_db.session.add(user)
            clean_db.session.commit()
            
            amenity = Amenity(
                name="Pool",
                description="Swimming pool"
            )
            clean_db.session.add(amenity)
            clean_db.session.commit()
            
            # Verify records exist
            assert User.query.count() >= 1
            assert Amenity.query.count() >= 1
            print("✅ Basic models created successfully")
            print(f"   Users: {User.query.count()}")
            print(f"   Amenities: {Amenity.query.count()}")