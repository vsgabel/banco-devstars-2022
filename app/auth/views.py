from flask_login import login_required, login_user, logout_user, current_user
from app.auth import auth
from flask import redirect, render_template, request, url_for, current_app
from ..models import User
from app.util import Serializer

@auth.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route("/do_login", methods=['POST'])
def do_login():
    if request.form:
        user = User.query.filter_by(email=request.form['usr']).first()
        if user and user.verify_password(request.form['pwd']):
            login_user(user)
            return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/token")
@login_required
def token():
    return Serializer.generate_token(current_app.config['SECRET_KEY'],
                                    current_user.id)
