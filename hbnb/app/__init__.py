from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Creates extension instances so they can be used everywhere
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__) # Creates new flask app
    app.config.from_object(config_class) # Loads config settings from config.py
    
    # JWT secret key to "sign" tokens (like a stamp)
    app.config['JWT_SECRET_KEY'] = 'this-is-our-secret-key-for-hbnb-yay'
    
    # Connect extensions to this flask app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Create database tables
    with app.app_context():
        try:
            print("🔍 Creating database tables...")
            print(f"🔗 Database URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
            
            # import pivot tables
            print("📦 Importing pivot tables...")
            from app.models.pivot_table import place_amenity

            # Import models AFTER app context is established
            print("📦 Importing models...")
            from app.models.user import User
            from app.models.amenity import Amenity
            from app.models.place import Place
            from app.models.review import Review
            print("📦 Models imported successfully!")
            
            # Test database connection (new SQLAlchemy way)
            with db.engine.connect() as conn:
                result = conn.execute(db.text('SELECT 1'))
                print("✅ Database connection successful!")
            
            # Create tables
            db.create_all()
            print("✅ db.create_all() executed!")
            
            # Check what tables were created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Tables in database: {tables}")

        except Exception as e:
            print(f"❌ Error during table creation: {e}")
            import traceback
            traceback.print_exc()

    # Import namespaces after app context is established
    print("Importing namespaces...")
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns

    # creates restapi attached to the flask
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/')

    # Register all namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app