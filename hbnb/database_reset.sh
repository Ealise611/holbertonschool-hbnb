
# Can reset both development and testing databases

# How to use:
#    python3 reset_db.py              Reset development database
#    python3 reset_db.py --test       Reset testing database  
#    python3 reset_db.py --both       Reset both databases

import sys
import argparse
from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

def reset_development_database():
    """Reset the development database and add initial data"""
    print("Resetting DEVELOPMENT database (hbnb_db)...")
    app = create_app('DevelopmentConfig')
    
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        
        print("Creating all tables...")
        db.create_all()
        
        print("Adding initial development data...")
        
        # Create admin user
        admin = User(
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            is_admin=True
        )
        admin.hash_password('admin1234')
        db.session.add(admin)
        
        # Create initial amenities
        amenities = [
            Amenity(name='WiFi', description='High-speed wireless internet'),
            Amenity(name='Swimming Pool', description='Outdoor swimming pool'),
            Amenity(name='Air Conditioning', description='Central air conditioning')
        ]
        
        for amenity in amenities:
            db.session.add(amenity)
        
        try:
            db.session.commit()
            print("Development database reset completed successfully!")
            print("Admin user: admin@hbnb.io / admin1234")
            print("Amenities: WiFi, Swimming Pool, Air Conditioning")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            return False

def reset_testing_database():
    """Reset the testing database and add test data"""
    print("Resetting TESTING database (hbnb_test_db)...")
    app = create_app('TestingConfig')
    
    with app.app_context():
        print("Dropping all test tables...")
        db.drop_all()
        
        print("Creating all test tables...")
        db.create_all()
        
        print("Adding initial test data...")
        
        # Create test admin user
        admin = User(
            first_name='Test',
            last_name='Admin',
            email='test.admin@hbnb.io',
            is_admin=True
        )
        admin.hash_password('testadmin123')
        db.session.add(admin)
        
        # Create test regular user
        regular_user = User(
            first_name='Test',
            last_name='User',
            email='test.user@hbnb.io',
            is_admin=False
        )
        regular_user.hash_password('testuser123')
        db.session.add(regular_user)
        
        # Create test amenities
        test_amenities = [
            Amenity(name='Test WiFi', description='WiFi for testing'),
            Amenity(name='Test Pool', description='Swimming pool for testing'),
            Amenity(name='Test AC', description='Air conditioning for testing'),
            Amenity(name='Test Parking', description='Parking for testing'),
            Amenity(name='Test Kitchen', description='Kitchen facilities for testing')
        ]
        
        for amenity in test_amenities:
            db.session.add(amenity)
        
        try:
            db.session.commit()
            print("Testing database reset completed successfully!")
            print("Test Admin: test.admin@hbnb.io / testadmin123")
            print("Test User: test.user@hbnb.io / testuser123")
            print("Test Amenities: Test WiFi, Test Pool, Test AC, Test Parking, Test Kitchen")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            return False

def reset_both_databases():
    """Reset both development and testing databases"""
    print("Resetting BOTH databases...")
    
    dev_success = reset_development_database()
    print("\n" + "="*60 + "\n")
    test_success = reset_testing_database()
    
    if dev_success and test_success:
        print("\nBoth databases reset successfully!")
        return True
    else:
        print("\nSome databases failed to reset")
        return False

def main():
    """Main function with argument parsing"""
    parser = argparse.ArgumentParser(description='Reset HBnB databases')
    parser.add_argument('--test', action='store_true', 
                       help='Reset testing database only')
    parser.add_argument('--dev', action='store_true', 
                       help='Reset development database only') 
    parser.add_argument('--both', action='store_true',
                       help='Reset both databases')
    
    args = parser.parse_args()
    
    # If no arguments, default to development
    if not any([args.test, args.dev, args.both]):
        print("No database specified, resetting development database...")
        print("Use --test for testing DB, --both for both databases")
        success = reset_development_database()
    elif args.test:
        success = reset_testing_database()
    elif args.dev:
        success = reset_development_database()
    elif args.both:
        success = reset_both_databases()
    else:
        print("Invalid arguments")
        parser.print_help()
        return False
    
    return success

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)