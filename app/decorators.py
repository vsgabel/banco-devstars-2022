from functools import wraps
from .models import Permission
from flask import abort
from flask_login import current_user

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.role.has_permission(permission):
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

def criar_required(f):
    decorador = permission_required(Permission.CRIAR)
    return decorador(f)

def alterar_required(f):
    decorador = permission_required(Permission.ALTERAR_LIMITE)
    return decorador(f)

def desabilitar_required(f):
    decorador = permission_required(Permission.DESABILITAR)
    return decorador(f)



# Código Simples de Decorador
# @wraps(f)
# def decorated_function(*args, **kwargs):
#     if not current_user.role.has_permission(Permission.CRIAR + Permission.ALTERAR_LIMITE + Permission.DESABILITAR):
#         return abort(403)
#     return f(*args, **kwargs)
# return decorated_function
            