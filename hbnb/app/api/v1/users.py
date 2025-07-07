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

# Admin user model (can modify everything including admin status)
admin_user_model = api.model('AdminUser', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(description='Admin privileges')
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
    @api.expect(profile_model) 
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered or invalid input data')
    def put(self, user_id):
        """Update user by ID - ONLY AUTH USER CAN UPDATE THEIR OWN DETAILS"""
        current_user = get_jwt_identity()
        is_admin = current_user.get('is_admin', False)
        
        # Admins can modify any user, regular users only their own
        if not is_admin and current_user['id'] != user_id:
            return {'error': 'Unauthorised action'}, 403
        
        data = api.payload
        
        # Only admins can change email, password, or admin status
        if not is_admin and ('email' in data or 'password' in data or 'is_admin' in data):
            return {'error': 'You cannot modify email, password, or admin status'}, 400
        
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            
            # Admins can change email, check for uniqueness
            if is_admin and 'email' in data and data['email'] != user.email:
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user:
                    return {'error': 'Email already in use'}, 400

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

# ADMIN ONLY USER CREATION
@api.route('/admin')
class AdminUserList(Resource):
    @jwt_required()
    @api.expect(admin_user_model, validate=True)
    @api.response(201, 'User created by admin')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Admin: Create a new user (can set admin privileges)"""
        current_user = get_jwt_identity()
        
        # Check if current user is admin
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload

        try:
            # Check for duplicate email
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400

            # Admin can create users with admin privileges
            new_user = facade.create_user(user_data)
            
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin
            }, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400