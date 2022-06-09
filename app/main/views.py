from flask import redirect, url_for
from flask_login import login_required, current_user
from app.main import main
from ..decorators import admin_required

@main.route("/")
@login_required
def index():
    return "funcionou"

@main.route("/perfil")
@login_required
def perfil():
    return f"""
    <p>{current_user.nome}</p>
    <p>{current_user.cpf}</p>
    """

@main.route("/admin")
@login_required
@admin_required
def admin():
    return "Página de administração"