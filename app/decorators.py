from functools import wraps
from .models import Permission
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.role.has_permission(Permission.ADMIN):
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
            