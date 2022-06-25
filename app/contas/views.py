from flask import redirect, render_template, request, url_for
from app import db
from app.contas import contas
from app.decorators import permission_required
from app.models import Permission, Conta
from flask_login import login_required, current_user

@contas.route("/")
def index():
    contas = Conta.query.filter_by(titular_id=current_user.id, enabled=True).all()
    tipo = "padrão"
    if current_user.role.has_permission(Permission.ADMIN):
        contas = Conta.query.all()
        tipo = "admin"

    return render_template("contas/index.html", contas=contas, tipo=tipo)

@contas.route("/desabilitar/<id>")
@login_required
@permission_required(Permission.DESABILITAR)
def desabilitar(id):
    conta = Conta.query.filter_by(id=id, enabled=True).first()
    if conta:
        conta.enabled = False

        db.session.add(conta)
        db.session.commit()

        return redirect(url_for("contas.index"))
    return redirect(url_for("contas.index"))

@contas.route("/habilitar/<id>")
@login_required
@permission_required(Permission.DESABILITAR)
def habilitar(id):
    conta = Conta.query.filter_by(id=id, enabled=False).first()
    if conta:
        conta.enabled = True

        db.session.add(conta)
        db.session.commit()

        return redirect(url_for("contas.index"))
    return redirect(url_for("contas.index"))

@contas.route("/criar", methods=["GET", "POST"])
@login_required
@permission_required(Permission.CRIAR)
def criar():
    if request.form:
        conta = Conta()
        conta.saldo = request.form.get("saldo")
        conta.titular_id = current_user.id

        db.session.add(conta)
        db.session.commit()

        return redirect(url_for("contas.index"))
    return render_template("contas/criar.html")