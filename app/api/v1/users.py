from math import perm
from app.api.v1 import api_v1
from flask import abort, jsonify, request
from app.models import User, Permission
from .authentication import auth
from .decorators import permission_required
from app import db
from app.util import requisitos

@api_v1.route("/usuarios")
@auth.login_required
@permission_required(Permission.ADMIN)
def usuarios():
    users_raw = User.query.all()
    users = []
    for u in users_raw:
        users.append(u.to_dict())

    '''
    # MÉTODO ALTERNATIVO QUE USA MENOS
    # MEMÓRIA
    for i in range(len(users)):
        users[i] = users[i].to_dict()
    '''

    return jsonify(users)

@api_v1.route("/usuario", methods=["POST"])
def cria_usuario():
    dados = request.get_json()
    obrigatorios = ['nome', 'cpf', 'email', 'senha']

    requisitos(obrigatorios, dados.keys())

    if len(dados['cpf']) != 11:
        return jsonify({"status": "error", "message": "CPF inválido"})

    ver = User.query.filter_by(cpf=dados['cpf']).first()
    if ver:
        return jsonify({"status": "error", "message": "O CPF já está cadastrado."})

    ver = User.query.filter_by(email=dados['email']).first()
    if ver:
        return jsonify({"status": "error", "message": "O e-mail já está cadastrado."})

    u = User()
    u.nome = dados['nome']
    u.cpf = dados['cpf']
    u.email = dados['email']
    u.senha = dados['senha']

    try:
        db.session.add(u)
        db.session.commit()
    except:
        return jsonify({"status": "error", "message": "Ocorreu um erro no servidor"}, 500)

    return jsonify({"status": "success", "message": "Usuário cadastrado com sucesso!"}, 200)