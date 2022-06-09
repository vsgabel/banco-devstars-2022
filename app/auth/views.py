from flask_login import login_user, logout_user
from app.auth import auth
from flask import redirect, render_template, request, url_for
from ..models import User

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
