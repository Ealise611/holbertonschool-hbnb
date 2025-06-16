# How to Run Tests

## Quick Testing (for debugging)

```bash
# Run from hbnb/ directory
cd hbnb

# Quick test to verify everything works
python tests/quick_test.py

# Run all tests with summary
python tests/test_all_simple.py
```

## Individual Model Tests

```bash
# Test specific models
python tests/test_models/test_user.py
python tests/test_models/test_place.py
python tests/test_models/test_review.py
python tests/test_models/test_amenity.py
python tests/test_models/test_base_model.py
```

## Test File Structure

### Basic Test File Template

```python
#!/usr/bin/env python3
"""Test [ModelName] model"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.your_model import YourModel

def test_model_creation():
    """Test basic model creation"""
    model = YourModel(param1="value1", param2="value2")
    
    assert model.param1 == "value1"
    assert model.param2 == "value2"
    assert hasattr(model, 'id')  # From BaseModel
    print("✅ Model creation test passed!")

def test_model_validation():
    """Test model validation"""
    try:
        # This should fail
        invalid_model = YourModel(param1="", param2="invalid")
        print("❌ Validation should have failed")
    except ValueError as e:
        print(f"✅ Validation works: {e}")

if __name__ == "__main__":
    test_model_creation()
    test_model_validation()
    print("✅ All tests passed!")
```

## Debugging Failed Tests

### 1. Read the Error Message

```bash
# Error shows exactly what failed
❌ Test failed: Title is required and must be ≤ 100 characters
```

### 2. Use Print Statements

```python
def test_something():
    print(f"Testing with value: {test_value}")
    result = some_function(test_value)
    print(f"Got result: {result}")
    assert result == expected
```

### 3. Test Incrementally

```bash
# Test one model at a time
python tests/test_models/test_user.py
```

### 4. Check Imports

```python
# Add this to test import issues
try:
    from app.models.user import User
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")
```

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Make sure you're in the right directory
cd hbnb
python tests/quick_test.py
```

**Module Not Found:**
```bash
# Install missing dependencies
pip install -r requirements.txt
```

**Path Issues:**
```bash
# Check your project structure matches the expected layout
ls -la app/models/
```