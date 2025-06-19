"""
Base test class with common setup for all tests
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.services import facade


class BaseTestCase(unittest.TestCase):
    """Base test case with repository cleanup"""
    
    def setUp(self):
        """Set up test client and clear repositories"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Clear all repositories before each test
        self.clear_repositories()
    
    def tearDown(self):
        """Clean up after each test"""
        self.clear_repositories()
    
    def clear_repositories(self):
        """Clear all repository storage"""
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()
        facade.review_repo._storage.clear()
        facade.amenity_repo._storage.clear()