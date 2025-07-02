from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    
# Protected endpoint that requires tokens
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required() # decorater to look for jwt header, extract token, verify signature using secret key, if token hasn't expired allows request to cont. else returns 401 unauth 
    def get(self):
        '''A protected endpoint that requires JWT token'''
        current_user = get_jwt_identity() # extracts user info from token, just id and is_admin
        return {
            'message': f'Hello user {current_user["id"]}!',
            'user_data': current_user
        }, 200