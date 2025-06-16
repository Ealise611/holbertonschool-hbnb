#!/usr/bin/env python3
"""Test BaseModel"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.base_model import BaseModel
from datetime import datetime
import uuid

def test_base_model_creation():
    """Test BaseModel creation and basic functionality"""
    base = BaseModel()
    
    # Test attributes exist
    assert hasattr(base, 'id')
    assert hasattr(base, 'created_at')
    assert hasattr(base, 'updated_at')
    
    # Test ID is string UUID
    assert isinstance(base.id, str)
    # Should not raise exception if valid UUID
    uuid.UUID(base.id)
    
    # Test timestamps are datetime objects
    assert isinstance(base.created_at, datetime)
    assert isinstance(base.updated_at, datetime)
    
    # Test created_at and updated_at are initially the same
    assert base.created_at == base.updated_at
    
    print("BaseModel creation test passed!")

def test_base_model_save():
    """Test BaseModel save method"""
    base = BaseModel()
    original_updated_at = base.updated_at
    
    # Save should update the timestamp
    base.save()
    
    assert base.updated_at > original_updated_at
    print("BaseModel save test passed!")

def test_base_model_update():
    """Test BaseModel update method"""
    base = BaseModel()
    
    # Add a test attribute
    base.test_attr = "original"
    original_updated_at = base.updated_at
    
    # Update should change attribute and timestamp
    base.update({'test_attr': 'updated'})
    
    assert base.test_attr == 'updated'
    assert base.updated_at > original_updated_at
    print("BaseModel update test passed!")

def test_base_model_unique_ids():
    """Test that different instances have different IDs"""
    base1 = BaseModel()
    base2 = BaseModel()
    
    assert base1.id != base2.id
    print("BaseModel unique IDs test passed!")

if __name__ == "__main__":
    test_base_model_creation()
    test_base_model_save()
    test_base_model_update()
    test_base_model_unique_ids()
    print("✅ All BaseModel tests passed!")