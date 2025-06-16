#!/usr/bin/env python3
"""Simple test for BaseModel class"""

import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """Simple test cases for BaseModel class"""

    def test_base_model_creation(self):
        """Test BaseModel can be created"""
        base = BaseModel()
        
        self.assertIsNotNone(base.id)
        self.assertIsNotNone(base.created_at)
        self.assertIsNotNone(base.updated_at)
        print("✅ BaseModel creation works")

    def test_to_dict(self):
        """Test BaseModel to_dict method"""
        base = BaseModel()
        base_dict = base.to_dict()
        
        self.assertIn('id', base_dict)
        self.assertIn('created_at', base_dict)
        print("✅ BaseModel to_dict works")


if __name__ == '__main__':
    unittest.main()