from functools import wraps
from tkinter import EXCEPTION
from flask import g, abort, request
from app.util import requisitos

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user.role.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def campos_obrigatorios(campos, origem="JSON"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if origem == "JSON":
                dados = request.get_json()
            elif origem == "URL":
                dados = request.args
            elif origem == "FORM":
                dados = request.form
            else:
                raise Exception("Esta origem de dados não é válida.")
            requisitos(campos, dados.keys())
            return f(*args, **kwargs)
        return decorated_function
    return decorator