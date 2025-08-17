# HBnB Evolution

A full-stack property rental platform inspired by Airbnb, built with modern web technologies and clean architecture principles. This project demonstrates comprehensive software engineering practices including RESTful API development, layered architecture, and responsive web design.

![Python](https://img.shields.io/badge/Python-3.8+-brightgreen.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-orange.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue.svg)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)

## Project Overview

HBnB Evolution is a property rental platform that enables users to:

- **Browse and search properties** with advanced filtering options
- **Register and authenticate** with secure JWT-based authentication
- **Create and manage property listings** with detailed information and amenities
- **Submit and manage reviews** with rating systems
- **Administer platform content** with role-based access control

The system is built using a four-tier layered architecture ensuring maintainability, scalability, and separation of concerns.

## Key Features

### Property Management
- Create, read, update, and delete property listings
- Geographic coordinate validation and mapping
- Price filtering and search capabilities
- Amenity associations with many-to-many relationships

### User Management
- Secure user registration and authentication
- JWT token-based session management
- Role-based permissions (Admin/User)
- Profile management with validation

### Review System
- 1-5 star rating system with validation
- Comprehensive review text and user feedback
- Business rule enforcement (no self-reviews, one review per user per place)
- Review ownership and admin management

### Admin Features
- Admin-only amenity management
- User privilege administration
- System-wide content moderation
- Platform configuration management

## Architecture

### Layered Architecture
```
┌─────────────────────────────────────┐
│         Presentation Layer          │  ← REST API endpoints, validation
├─────────────────────────────────────┤
│           Facade Layer              │  ← Business logic coordination
├─────────────────────────────────────┤
│        Business Logic Layer         │  ← Core domain rules & workflows
├─────────────────────────────────────┤
│         Persistence Layer           │  ← Database operations & ORM
└─────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- **Python 3.8+** - Core programming language
- **Flask** - Lightweight web framework
- **Flask-RESTx** - API development with auto-documentation
- **SQLAlchemy** - Database ORM and modeling
- **MySQL** - Production database

**Frontend:**
- **HTML5** - Semantic markup and structure
- **CSS3** - Modern styling with gradients and animations
- **JavaScript ES6** - Client-side interactivity and API communication

**Security:**
- **Flask-JWT-Extended** - JSON Web Token authentication
- **Flask-Bcrypt** - Password hashing and verification
- **CORS** - Cross-origin resource sharing configuration

## Getting Started

### Prerequisites
```bash
Python 3.8+
MySQL 5.7+
pip package manager
```

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd hbnb-evolution
```

2. **Set up the backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure MySQL database**
```bash
# Install and start MySQL
sudo apt update
sudo apt install mysql-server
sudo service mysql start

# Configure MySQL root user
mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';"

# Create databases
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS hbnb_db;"
mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS hbnb_test_db;"
```

4. **Initialize the database**
```bash
python setup_test_db.py
```

5. **Start the backend server**
```bash
python run.py
```
### Docker Setup (recommended)

```bash
# Build and run with Docker Compose
docker-compose build
docker-compose up
```

6. **Serve the frontend**
```bash
cd ../front_end
# Serve files using any web server, e.g.:
python -m http.server 3000
# or
npx serve -p 3000
```


This will set up:
- MySQL database on port 3307
- Flask API on port 5000
- Automatic database initialization

## API Documentation

### Interactive Documentation
Visit `http://localhost:5000/` when running the application to access the Swagger UI with:
- Interactive API explorer for testing endpoints
- Request/response schemas with validation rules
- Authentication flows with JWT token management

### Core API Endpoints

#### Authentication
```http
POST /api/v1/auth/login           # User login with JWT token generation
POST /api/v1/auth/create-admin    # Create initial admin user (development)
```

#### User Management
```http
GET  /api/v1/users/              # List all users (public)
POST /api/v1/users/              # Register new user (public)
GET  /api/v1/users/{id}          # Get user details (public)
PUT  /api/v1/users/{id}          # Update user profile (owner/admin)
POST /api/v1/users/admin         # Create admin user (admin only)
```

#### Place Management
```http
GET  /api/v1/places/             # List all places (public)
POST /api/v1/places/             # Create new place (authenticated)
GET  /api/v1/places/{id}         # Get place details (public)
PUT  /api/v1/places/{id}         # Update place (owner/admin)
```

#### Review Management
```http
GET    /api/v1/reviews/          # List all reviews (public)
POST   /api/v1/reviews/          # Create review (authenticated)
PUT    /api/v1/reviews/{id}      # Update review (author/admin)
DELETE /api/v1/reviews/{id}      # Delete review (author/admin)
```

#### Amenity Management
```http
GET /api/v1/amenities/           # List all amenities (public)
POST /api/v1/amenities/          # Create amenity (admin only)
PUT /api/v1/amenities/{id}       # Update amenity (admin only)
```

## Security Features

### Authentication & Authorization
- **JWT-based authentication** with secure token management
- **Password hashing** using bcrypt with salt
- **Role-based access control** (regular users vs administrators)
- **Token expiration** with configurable timeouts

### Data Protection
- **Input validation** preventing injection attacks
- **Business rule enforcement** preventing unauthorized actions
- **Password exclusion** from all API responses
- **CORS configuration** for secure cross-origin requests

### Dummy Data Setup
```bash
# Create comprehensive test data
python setup_test_data.py
```

This creates:
- 4 test users with varied roles
- 17 properties across different price ranges
- 7 amenities for comprehensive testing
- 15+ cross-reviews between users

## Frontend Features

### Responsive Design
- **Mobile-first approach** with responsive grid layouts
- **Modern CSS** with gradients, animations, and glassmorphism effects
- **Accessibility features** with proper semantic markup

### User Experience
- **Price filtering** with multiple range options ($10, $50, $100, All)
- **Real-time authentication** status management
- **Dynamic content loading** without page refreshes
- **Error handling** with user-friendly messages

### Pages & Functionality
- **Login page** with JWT token management
- **Property listings** with filtering and search
- **Property details** with reviews and amenities
- **Review submission** for authenticated users

## Business Rules

### User Validation
- Email format validation with regex patterns
- Email uniqueness enforced at database level
- Password security with bcrypt hashing
- Name length constraints (max 50 characters)

### Property Validation
- Title requirements (non-empty, max 100 characters)
- Price validation (must be positive numeric values)
- Geographic constraints (latitude: -90 to 90, longitude: -180 to 180)
- Owner validation (must reference existing user)

### Review Validation
- Rating constraints (integer values 1-5 only)
- Text requirements (non-empty review content)
- Business rules (users cannot review their own places)
- Uniqueness (one review per user per place maximum)

## Project Structure

```
hbnb-evolution/
├── backend/                     # Flask API backend
│   ├── app/
│   │   ├── api/v1/             # REST API endpoints
│   │   ├── models/             # Database models
│   │   ├── services/           # Business logic layer
│   │   ├── persistence/        # Data access layer
│   │   └── utils/              # Utility functions
│   ├── pytest_tests/          # Comprehensive test suite
│   ├── requirements.txt        # Python dependencies
│   └── run.py                  # Application entry point
├── front_end/                  # Frontend web client
│   ├── index.html              # Property listings page
│   ├── login.html              # User authentication
│   ├── place.html              # Property details
│   ├── add_review.html         # Review submission
│   ├── styles.css              # Modern CSS styling
│   └── scripts.js              # Client-side JavaScript
├── docker-compose.yml          # Container orchestration
└── README.md                   # Project documentation
```

## Contributors

This project was developed by:

- **[Ealise Wang](https://github.com/ealise-wang)**
- **[Kassandra Iatrou](https://github.com/kassandra-iatrou)**
- **[Sammy Hill](https://github.com/sammy-hill)**

## Academic Context

HBnB Evolution was developed as part of the Holberton School software engineering curriculum, demonstrating:

- **Full-stack web development** skills
- **RESTful API design** and implementation
- **Database design** and ORM usage
- **Security best practices** in web applications
- **Modern frontend development** techniques
- **Testing and quality assurance** methodologies
- **Docker containerization** and deployment

---