from app import db
from app.api.v1 import api_v1
from flask import jsonify, request, g
from app.models import Cartao, Permission
from .authentication import auth
from .decorators import campos_obrigatorios, permission_required

@api_v1.route("/cartao", methods=['POST'])
@auth.login_required
@permission_required(Permission.CRIAR)
@campos_obrigatorios(['titular_id', 'limite'])
def cria_cartao():
    dados = request.get_json()
    cartao = Cartao()
    cartao.user_id = dados['titular_id']
    cartao.limite = dados['limite']

    db.session.add(cartao)
    db.session.commit()

    return jsonify({"status": "success", "message": "Cartão criada com sucesso"})

@api_v1.route("/cartoes")
@auth.login_required
@campos_obrigatorios(['titular_id'], "URL")
def pega_cartoes():
    dados = request.args
    cartoes = Cartao.query.filter_by(user_id=dados['titular_id'], enabled=True).all()
    lista = []
    for cartao in cartoes:
        lista.append(cartao.to_dict())

    return jsonify({"status": "success", "message": "", "data": lista})