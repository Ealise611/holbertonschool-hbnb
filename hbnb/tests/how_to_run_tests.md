# How to Run Tests

## Run Individual Tests
```bash
cd hbnb/
python3 tests/test_user.py
python3 tests/test_amenity.py
python3 tests/test_place.py
python3 tests/test_review.py
```

## Run All Tests
```bash
cd hbnb/
python3 tests/run_all_tests.py
```

## Expected Output
**Success:**
```
Ran x tests xs
OK
```

**Failure example:**
```
FAIL: test_create_user_invalid_email
AssertionError: 400 != 201
```