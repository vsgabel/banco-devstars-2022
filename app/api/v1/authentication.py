from flask_httpauth import HTTPTokenAuth
from flask import g, current_app
from app.util import Serializer

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(token):
    if token:
        u = Serializer.verify_auth_token(current_app.config['SECRET_KEY'], token)
        if u:
            g.current_user = u
            return True
    return False
# def verify_password(email, senha):
#     if not email:
#         return False
    
#     u = User.query.filter_by(email=email).first()
#     if not u:
#         return False

#     g.current_user = u
#     return u.verify_password(senha)
    
