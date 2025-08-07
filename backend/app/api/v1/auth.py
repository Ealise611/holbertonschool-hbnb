from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# This is what our login requests should look like
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

#login endpoint tha tcreates tokens
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        '''User login - get the JWT token'''
        credentials = api.payload # gets the JSON data from the request
        # Find user by email
        user = facade.get_user_by_email(credentials['email'])
        # Check if user exists and pass is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401
        # Create JWT toekn with user info
        access_token = create_access_token(
            identity={
                'id': str(user.id),
                'is_admin': user.is_admin
            }
        )
        # Send token back to user
        return {'access_token': access_token}, 200

@api.route('/create-admin')  # REMOVE THIS IN PRODUCTION!
class CreateAdmin(Resource):
    def post(self):
        """Create first admin user (TEMPORARY - remove in production!)"""
        admin_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@hbnb.io',
            'password': 'admin123',
            'is_admin': True
        }
        
        existing_admin = facade.get_user_by_email(admin_data['email'])
        if existing_admin:
            return {'error': 'Admin already exists'}, 400
        
        try:
            admin_user = facade.create_user(admin_data)
            return {
                'message': 'Admin user created successfully',
                'email': admin_user.email,
                'is_admin': admin_user.is_admin,
                'note': 'Use email: admin@hbnb.io, password: admin123 to login'
            }, 201
        except Exception as e:
            return {'error': f'Failed to create admin: {str(e)}'}, 500
