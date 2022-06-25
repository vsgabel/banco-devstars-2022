from app import db
from app.api.v1 import api_v1
from flask import jsonify, request, g
from app.models import Conta, Permission
from app.util import requisitos
from .authentication import auth
from .decorators import campos_obrigatorios, permission_required

@api_v1.route("/depositar", methods=['PUT'])
@campos_obrigatorios(['conta', 'valor'])
def depositar():
    dados = request.get_json()

    valor = float(dados['valor'])
    conta = Conta.query.filter_by(id=dados['conta'], enabled=True).first()
    if not conta:
        return jsonify({"status": "error", "message": "A conta não pode ser encontrada"})

    return jsonify(conta.depositar(valor))

@api_v1.route("/sacar", methods=['PUT'])
@auth.login_required
@permission_required(Permission.USAR)
@campos_obrigatorios(['conta', 'valor'])
def sacar():
    dados = request.get_json()

    valor = float(dados['valor'])
    conta = Conta.query.filter_by(id=dados['conta'], enabled=True).first()
    if not conta:
        return jsonify({"status": "error", "message": "A conta não pode ser encontrada"})
    
    if not conta.titular_id == g.current_user.id:
        return jsonify({"status": "error", "message": "Não possui autorização para sacar desta conta."})

    return jsonify(conta.sacar(valor))

@api_v1.route("/transferir", methods=['PUT'])
@auth.login_required
@permission_required(Permission.USAR)
@campos_obrigatorios(['conta_saida', 'conta_entrada', 'valor'])
def transferir():
    dados = request.get_json()

    conta_saida = Conta.query.filter_by(id=dados['conta_saida'], enabled=True).first()
    conta_entrada = Conta.query.filter_by(id=dados['conta_entrada'], enabled=True).first()
    if conta_saida.titular_id == g.current_user.id:
        return jsonify(Conta.transfere(conta_saida, conta_entrada, dados['valor']))
    return jsonify({"status": "error", "message": "Você não é titular da conta de saída"})
    

    