'''
Tests database setup for hbnb    
'''

import pymysql
import sys
import os

# add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity

def create_test_database():
    '''Creates the tests database'''
    try:
        print("Setting up test database...")
        
        #connect to MySQL without specifying database
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='root'
        )
        cursor = connection.cursor()
        
        cursor.execute("DROP DATABASE IF EXISTS hbnb_test_db")
        print("Created test database: hbnb_test_db")
        
        cursor.execute("CREATE DATABASE hbnb_test_db")
        print("Created test database: hbnb_test_db")
        
        cursor.execute("SHOW DATABASES LIKE 'hbnb_test_db'")
        result = cursor.fetchone()
        if result:
            print(f"Verified database exists: {result[0]}")
            
        cursor.close()
        connection.close()
        return True
    
    except Exception as e:
        print(f"Database creation failed: {e}")
        return False
    
def initialise_test_data():
    """initialises with some basic test data"""
    try:
        print("Initialising test data...")
        
        app = create_app('TestingConfig')
        
        with app.app_context():
            print("Tables already created by create_app")
            
            # Create test admin user
            admin = User(
                first_name='Test',
                last_name='Admin',
                email='test.admin@hbnb.io',
                password='testadmin123',
                is_admin=True
                )
            
            admin.hash_password('testadmin123')
            db.session.add(admin)
            print("Created test admin user")
            
            test_amenities = [
                Amenity(name='Test WiFi', description='WiFi for testing'),
                Amenity(name='Test Pool', description='Swimming pool for testing'),
                Amenity(name='Test AC', description='Air conditioning for testing')
            ]
            
            for amenity in test_amenities:
                db.session.add(amenity)
            print("Created test amenities")
            
            db.session.commit()
            print("Test data committed to database")
            
            user_count = db.session.query(User).count()
            amenity_count = db.session.query(Amenity).count()
            print(f"Test data summary: {user_count} users, {amenity_count} amenities")
            
        return True
    
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
def main():
    """Main setup function"""
    print("Starting test database setup...")
    
    if not create_test_database():
        print("Failed to create")
        return False
    
    if not initialise_test_data():
        print("failed to initialise data")
        return False
    
    print("\n yay! Test database setup completed successfully!")
    print("   Setup Summary:")
    print("   Database: hbnb_test_db")
    print("   Admin User: test.admin@hbnb.io / testadmin123")
    print("   Test Amenities: Test WiFi, Test Pool, Test AC")
    print("\n You can now run tests with: pytest pytest_tests/ -v")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
