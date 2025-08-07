from functools import wraps  # Preserves original function metadata
from flask_jwt_extended import get_jwt_identity

def admin_required(f):  # f is the function being decorated
    @wraps(f)  # Keeps original function name, docstring, etc.
    def decorated_function(*args, **kwargs):  # Wrapper function
        current_user = get_jwt_identity()  # Get user from JWT token
        
        # Check if user has admin privileges
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        # If admin, call the original function
        return f(*args, **kwargs)
    return decorated_function  # Return the wrapper