# HBnB Evolution Project

A full-stack Python application inspired by Airbnb, featuring user authentication, property management, and review systems. Built with Flask, SQLAlchemy, and MySQL, following clean architecture principles with layered design and comprehensive API documentation.

---

## Project Overview

HBnB Evolution is a property rental platform that enables users to:

- **Register and authenticate** with JWT-based security
- **Create and manage property listings** with detailed information
- **Browse and search properties** with location and amenity filtering
- **Submit and manage reviews** with rating systems
- **Administer platform content** with role-based access control

The system manages four core entities with rich relationships:
- **Users** (hosts, guests, and administrators)
- **Places** (property listings with location and pricing)
- **Amenities** (property features and services)
- **Reviews** (user feedback with ratings and comments)

---

## Architecture & Design

### Layered Architecture
The application follows a **four-tier layered architecture** ensuring clean separation of concerns:

- **Presentation Layer** - RESTful API endpoints with Flask-RESTx
- **Facade Layer** - Simplified interfaces hiding system complexity
- **Business Logic Layer** - Core domain rules and validation
- **Persistence Layer** - Database operations with SQLAlchemy ORM

### Key Design Patterns
- **Facade Pattern** - Centralized business logic coordination
- **Repository Pattern** - Abstracted data access layer
- **Decorator Pattern** - Clean authentication and authorization
- **MVC Architecture** - Clear separation of concerns

---

## Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask** - Lightweight web framework
- **Flask-RESTx** - API development with auto-generated documentation
- **SQLAlchemy** - Database ORM and modeling
- **Flask-SQLAlchemy** - Flask integration for database operations

### Security & Authentication
- **Flask-JWT-Extended** - JSON Web Token authentication
- **Flask-Bcrypt** - Password hashing and verification
- **Role-based Access Control** - Admin and user permission management

### Database
- **MySQL** - Production database (with PyMySQL connector)
- **Database Migrations** - Schema versioning and updates

### Development & Testing
- **pytest** - Testing framework with MySQL integration
- **cURL & Postman** - API testing and validation
- **Swagger UI** - Interactive API documentation

---

## Project Structure

```plaintext
hbnb/
├── app/
│   ├── api/                          # REST API endpoints
│   │   └── v1/
│   │       ├── auth.py               # Authentication (login, JWT tokens)
│   │       ├── users.py              # User management (CRUD, profiles)
│   │       ├── places.py             # Property listings (CRUD, search)
│   │       ├── amenities.py          # Amenity management (admin only)
│   │       └── reviews.py            # Review system (CRUD, ratings)
│   ├── models/                       # Database models and business logic
│   │   ├── base_model.py             # Base model with UUID and timestamps
│   │   ├── user.py                   # User model with authentication
│   │   ├── place.py                  # Place model with validations
│   │   ├── amenity.py                # Amenity model
│   │   ├── review.py                 # Review model with rating validation
│   │   └── pivot_table.py            # Many-to-many relationship tables
│   ├── services/
│   │   └── facade.py                 # Business logic coordination layer
│   ├── persistence/
│   │   └── repository.py             # Database abstraction layer
│   └── utils/
│       └── decorators.py             # Authentication decorators
├── pytest_tests/                     # Comprehensive test suite
├── config.py                         # Application configuration
├── requirements.txt                  # Project dependencies
├── run.py                            # Application entry point
└── setup_test_db.py                  # Database initialization script
```

---

## Features

### Authentication & Authorization
- **JWT-based authentication** with secure token management
- **Password hashing** using bcrypt for security
- **Role-based access control** (regular users vs administrators)
- **Protected endpoints** with proper permission validation

### User Management
- **User registration** with email validation and uniqueness
- **Profile management** with update capabilities
- **Admin user creation** with privilege assignment
- **Public user browsing** for transparency

### Property Management
- **Place creation** with comprehensive property details
- **Location validation** with latitude/longitude constraints
- **Price validation** ensuring positive values
- **Amenity associations** with many-to-many relationships
- **Owner-based permissions** for property modifications

### Review System
- **Rating system** with 1-5 star validation
- **Review ownership** ensuring users can only modify their reviews
- **Business rule enforcement** preventing self-reviews
- **Duplicate review prevention** one review per user per place

### Content Management
- **Admin-only amenity management** for platform consistency
- **Place-review relationships** with automatic associations
- **Data integrity** through foreign key constraints
- **Soft deletion** capabilities where appropriate

---

## API Endpoints

### Authentication
```http
POST /api/v1/auth/login           # User login with JWT token generation
POST /api/v1/auth/create-admin    # Create initial admin user (development)
```

### User Management
```http
GET  /api/v1/users/              # List all users (public)
POST /api/v1/users/              # Register new user (public)
GET  /api/v1/users/{id}          # Get user details (public)
PUT  /api/v1/users/{id}          # Update user profile (owner/admin)
POST /api/v1/users/admin         # Create user with admin privileges (admin only)
```

### Place Management
```http
GET  /api/v1/places/             # List all places (public)
POST /api/v1/places/             # Create new place (authenticated)
GET  /api/v1/places/{id}         # Get place details with owner and amenities (public)
PUT  /api/v1/places/{id}         # Update place (owner/admin)
GET  /api/v1/places/{id}/reviews # Get all reviews for a place (public)
```

### Review Management
```http
GET    /api/v1/reviews/          # List all reviews (public)
POST   /api/v1/reviews/          # Create review (authenticated, business rules)
GET    /api/v1/reviews/{id}      # Get review details (public)
PUT    /api/v1/reviews/{id}      # Update review (author/admin)
DELETE /api/v1/reviews/{id}      # Delete review (author/admin)
```

### Amenity Management
```http
GET /api/v1/amenities/           # List all amenities (public)
POST /api/v1/amenities/          # Create amenity (admin only)
GET /api/v1/amenities/{id}       # Get amenity details (public)
PUT /api/v1/amenities/{id}       # Update amenity (admin only)
```

---

## Business Rules & Validation

### User Validation
- **Email format validation** with regex pattern matching
- **Email uniqueness** enforced at database and application level
- **Password requirements** with secure hashing
- **Name validation** with length constraints (max 50 characters)

### Place Validation
- **Title requirements** non-empty, max 100 characters
- **Price validation** must be positive numeric value
- **Geographic constraints** latitude (-90 to 90), longitude (-180 to 180)
- **Owner validation** must reference existing user

### Review Validation
- **Rating constraints** integer values 1-5 only
- **Text requirements** non-empty review content
- **Ownership rules** users cannot review their own places
- **Uniqueness** one review per user per place maximum

### Amenity Validation
- **Name requirements** non-empty, max 50 characters
- **Admin restrictions** only administrators can create/modify

---

## Database Schema

### Core Entities
- **users** - User accounts with authentication and profile data
- **places** - Property listings with location and pricing
- **amenities** - Platform-managed property features
- **reviews** - User feedback with ratings and comments

### Relationships
- **User → Places** (one-to-many) - Users can own multiple properties
- **Place → Reviews** (one-to-many) - Places can have multiple reviews
- **User → Reviews** (one-to-many) - Users can write multiple reviews
- **Place ↔ Amenities** (many-to-many) - Places can have multiple amenities

### Constraints
- **Foreign key constraints** ensuring referential integrity
- **Unique constraints** on user emails and review combinations
- **Check constraints** for rating values and coordinate ranges

---

## Installation & Setup

### Prerequisites
```bash
Python 3.8+
MySQL 5.7+
pip package manager
```

### Database Setup
```bash
# Install MySQL and start service
sudo apt update
sudo apt install mysql-server
sudo service mysql start

# Configure MySQL root user
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"

# Create databases
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS hbnb_db;"
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS hbnb_test_db;"
```

### Application Installation
```bash
# Clone repository
git clone <repository-url>
cd hbnb

# Install dependencies
pip install -r requirements.txt

# Initialize database
python setup_test_db.py

# Run application
python run.py
```

---

## Usage Examples

### User Registration
```bash
curl -X POST "http://localhost:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe", 
  "email": "john.doe@example.com",
  "password": "securepassword123"
}'
```

### User Login
```bash
curl -X POST "http://localhost:5000/api/v1/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "securepassword123"
}'
```

### Create Place (Authenticated)
```bash
curl -X POST "http://localhost:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{
  "title": "Cozy Apartment",
  "description": "Beautiful apartment in city center",
  "price": 150.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "amenities": ["wifi-id", "pool-id"]
}'
```

### Submit Review (Authenticated)
```bash
curl -X POST "http://localhost:5000/api/v1/reviews/" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_JWT_TOKEN" \
-d '{
  "text": "Amazing place, highly recommended!",
  "rating": 5,
  "place_id": "place-uuid-here"
}'
```

---

## Configuration

### Environment Configurations
- **Development** - SQLite/MySQL with debug enabled
- **Testing** - Dedicated test database with isolated data
- **Production** - MySQL with optimized settings

### Key Settings
```python
# Database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/hbnb_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Security
SECRET_KEY = 'your-secret-key-here'
JWT_SECRET_KEY = 'your-jwt-secret-key'

# Application
DEBUG = True  # Development only
TESTING = False
```

---

## API Documentation

### Interactive Documentation
Visit `http://localhost:5000/` when running the application to access the Swagger UI with:
- **Interactive API explorer** for testing endpoints
- **Request/response schemas** with validation rules
- **Authentication flows** with JWT token management
- **Error response formats** with status codes

### Response Formats

**Success Response:**
```json
{
  "id": "uuid-string",
  "title": "Property Title",
  "price": 150.0,
  "owner": {
    "id": "owner-uuid",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com"
  }
}
```

**Error Response:**
```json
{
  "error": "Descriptive error message"
}
```

---

## Security Features

### Authentication Security
- **Password hashing** with bcrypt and salt
- **JWT token expiration** with configurable timeouts
- **Secure token transmission** via Authorization headers
- **Input validation** preventing injection attacks

### Authorization Controls
- **Role-based permissions** with admin/user distinction
- **Resource ownership** validation for modifications
- **Business rule enforcement** preventing unauthorized actions
- **Public endpoint security** with appropriate access levels

### Data Protection
- **Password exclusion** from all API responses
- **Email validation** with format and uniqueness checks
- **Input sanitization** preventing malicious data
- **Database constraints** ensuring data integrity

---

## Contributors

Built as part of Holberton School curriculum by:
- **Ealise Wang**
- **Kassandra Iatrou**
- **Sammy Hill**
