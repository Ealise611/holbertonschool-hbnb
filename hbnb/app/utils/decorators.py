from functools import wraps
from flask_jwt_extended import get_jwt_identity

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = get_jwt_identity()
        
        # Check if user has admin privileges
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        return f(*args, **kwargs)
    return decorated_function
