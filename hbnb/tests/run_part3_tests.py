"""
Run all Part 3 tests for Authentication & Admin functionality
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if __name__ == '__main__':
    # Define test modules for Part 3
    part3_test_modules = [
        'test_auth',
        'test_admin_users', 
        'test_admin_amenities',
        'test_admin_places',
        'test_admin_reviews',
        'test_password_hashing',
        'test_jwt_protection'
    ]
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add Part 3 tests
    for module in part3_test_modules:
        try:
            tests = loader.loadTestsFromName(module)
            suite.addTests(tests)
            print(f"✅ Loaded tests from {module}")
        except Exception as e:
            print(f"❌ Failed to load {module}: {e}")
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"PART 3 TEST SUMMARY - Authentication & Admin Features")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    
    # Show failed tests if any
    if result.failures:
        print(f"\nFAILED TESTS:")
        for test, traceback in result.failures:
            print(f"❌ {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print(f"\nERROR TESTS:")
        for test, traceback in result.errors:
            print(f"💥 {test}: {traceback.split('Exception:')[-1].strip()}")
    
    print(f"{'='*60}")
    
    # Exit with error code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)