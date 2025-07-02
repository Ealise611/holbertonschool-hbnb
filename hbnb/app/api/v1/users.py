from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade
from app.models.user import User

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

# profile update model (no email or pass for regular users)
profile_model = api.model('UserProfile', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid input data')
    def post(self):
        """Register a new user - PUBLIC ACCESS"""
        user_data = api.payload

        try:
            # Check for duplicate email BEFORE creating user
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            new_user = facade.create_user(user_data)
            
            return {
                'id': new_user.id, 
                'first_name': new_user.first_name, 
                'last_name': new_user.last_name, 
                'email': new_user.email
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve list of users - PUBLIC ACCESS"""
        users = facade.get_all_users()

        return [
            {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }
             for user in users
        ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID - PUBLIC ACCESS"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
                'id': user.id, 
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'email': user.email
        }, 200

    @jwt_required()
    @api.expect(profile_model, validate=True)  # Changed user_model → profile_model
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered or invalid input data')
    def put(self, user_id):
        """Update user by ID - ONLY AUTH USER CAN UPDATE THEIR OWN DETAILS"""
        current_user = get_jwt_identity()
        
        # ownership check
        if current_user['id'] != user_id:
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload
        
        # regular users can't change email or password, redundant but still good to have
        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400
        
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
    
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400