from functools import wraps  # Preserves original function metadata
from flask_jwt_extended import get_jwt_identity, get_jwt


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        if not claims.get("is_admin", False):
            return {"error": "Admin privileges required"}, 403

        return f(*args, **kwargs)

    return decorated_function
