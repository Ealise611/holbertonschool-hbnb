# HBnB Evolution Project

An educational full-stack Python project inspired by the Airbnb platform. This application manages users, places, reviews, and amenities using a layered architecture with clean separation between business logic, data persistence, and presentation (API).

---

## Project Overview

This project simulates a property listing platform, allowing users to create, retrieve, and manage entities such as:

- **Users** (hosts or reviewers)
- **Places** (properties listed by users)
- **Amenities** (features of a place)
- **Reviews** (user-generated feedback)

The system is organized into clean architectural layers using the **Facade Pattern**, and follows RESTful conventions with Flask-RESTx.

---

## Project Structure

```plaintext
holbertonschool-hbnb/
│
├── hbnb/
│   ├── app/
│   │   ├── api/                      # Flask-RESTx API routes
│   │   │   └── v1/
│   │   │       ├── __init__.py       
│   │   │       ├── amenities.py      # Flask-RESTx routes for amenity creation and retrieval
│   │   │       ├── places.py         # Flask-RESTx routes for place creation and retrieval
│   │   │       ├── reviews.py        # Flask-RESTx routes for review creation and retrieval
│   │   │       └── users.py          # Flask-RESTx routes for user creation and retrieval
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base_model.py         # Base model with UUIDs, timestamps, and update method
│   │   │   ├── amenity.py            # Amenity model with validation, inherits from BaseModel
│   │   │   ├── place.py              # Place model with owner, location, and amenity links
│   │   │   ├── review.py             # Review model linking user, place, rating, and text
│   │   │   └── user.py               # User model with validation for name and email
│   │   ├── persistance/              
│   │   │   └── repository.py         # Abstract repository and in-memory data storage implementation
│   │   ├── services/
│   │   │   ├── facade.py             # Central business logic coordinating all entity operations
│   │   │   └── facade_with_val.py    # Central business logic coordinating all entity operations with validation
│   │   └── validation/               # Validation files
│   │       ├── user_validation.py    # Validation rules for user creation and updates
│   │       ├── place_validation.py   # Validates place attributes like price, coordinates, and owner
│   │       ├── review_validation.py  # Ensures review text, rating, and relationships are valid
│   │       └── amenity_validation.py # Validates amenity name length and formatting rules
│   ├── tests/                        # Unit tests 
│   │   ├── base_test.py              # Base class for test setup and teardown
│   │   ├── how_to_run_tests.md       # Testing use instructions
│   │   ├── run_all_tests.py          # Run all test suites in the tests/ directory using unittest
│   │   ├── test_amenity.py           # Unit tests for the Amenity model and its API endpoints
│   │   ├── test_place                # Unit tests for the Place model and its API endpoints
│   │   ├── test_user.py              # Unit tests for the User model and its API endpoints
│   │   └── test_review.py            # Unit tests for the Review model and its API endpoints
│   ├── README.md                     # Poject README (this file)
│   ├── TESTING.md                    # Testing and validation documentation
│   ├── config.py                     # App configuration (Flask setup)
│   ├── requirements.txt              # Flask version requirements
│   └── run.py                        # File set-up
│
└── planning documentation/           # Documentation files (diagrams, UML, notes)
```

---

## Key Features

- Clean 3-layer architecture (Presentation, Business Logic, Persistence)
- RESTful API with Flask-RESTx
- Entity validation in the business logic layer
- In-memory repository implementation for fast testing
- Auto-generated Swagger docs
- Unit and black-box testing using unittest and Postman/cURL
- Fully documented testing strategy (TESTING.md)

---

## Technologies Used

- Python 3.8+
- Flask
- Flask-RESTx
- UUID for entity IDs
- unittest (Python’s built-in test framework)
- Postman & cURL for black-box API testing

---

## Testing Strategy

See hbnb/TESTING.md for full details.
Includes:
- Model-level validation testing
- Unit tests for all endpoints
- Postman collection-based black-box tests
- Swagger UI response validation

---

## Example API Usage

Create a User (via cURL):

```bash
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{
  "first_name": "Humphrey",
  "last_name": "Bear",
  "email": "humphrey.bear@example.com"
}'
```

Expected Response:

```json
{
  "id": "uuid-generated-id",
  "first_name": "Humphrey",
  "last_name": "Bear",
  "email": "humphrey.bear@example.com"
}
```

---

## Documentation

- Swagger UI: http://127.0.0.1:5000/
- README: [README.md](https://github.com/Ealise611/holbertonschool-hbnb/blob/Main/hbnb/README.md)
- Testing Strategy: [TESTING.md](https://github.com/Ealise611/holbertonschool-hbnb/blob/Main/hbnb/TESTING.md)
- Part 1 Diagrams and Notes: [Planning Documentation](https://github.com/Ealise611/holbertonschool-hbnb/tree/Main/planning%20documentation)

---

## Design Patterns

- Facade Pattern to decouple API from core business logic
- Repository Pattern for flexible data persistence
- Validation Layer for enforcing rules at the service level

---

## Contributors

Project built as part of Holberton School curriculum by:
- vernfleming
- ealise611
- CascadingDreams

---

## License

Feel free to do with this as you please.