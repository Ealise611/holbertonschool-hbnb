from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
#from app.api.v1.users import api as users_ns
#from app.api.v1.amenities import api as amenities_ns
#from app.api.v1.places import api as places_ns
#from app.api.v1.reviews import api as reviews_ns
#from app.api.v1.auth import api as auth_ns
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
    
    # Import models to register them with SQLAlchemy
    from app.models.user import User
    from app.models.amenity import Amenity
    from app.models.place import Place
    from app.models.review import Review
    
    #create database tables
    with app.app_context():
        print("Creating database tables...")
        db.create_all()  # Creates all tables in the database based on the models defined

    # creates restapi attached to the flask
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/')
    

    # Register all namespaces
    #api.add_namespace(users_ns, path='/api/v1/users')
    #api.add_namespace(amenities_ns, path='/api/v1/amenities')
    #api.add_namespace(places_ns, path='/api/v1/places')
    #api.add_namespace(reviews_ns, path='/api/v1/reviews')
    #api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app