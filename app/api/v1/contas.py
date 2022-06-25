from app import db
from app.api.v1 import api_v1
from flask import jsonify, request, g
from app.models import Conta, Permission
from app.util import requisitos
from .authentication import auth
from .decorators import permission_required

@api_v1.route("/depositar", methods=['PUT'])
def depositar():
    dados = request.get_json()
    obrigatorios = ['conta', 'valor']
    
    requisitos(obrigatorios, dados.keys())

    valor = float(dados['valor'])
    if valor > 0:
        conta = Conta.query.filter_by(id=dados['conta'], enabled=True).first()
        if conta:
            conta.saldo += valor
            db.session.add(conta)
            db.session.commit()

            return jsonify({"status": "success", "message": "Depósito efetuado"})
        return jsonify({"status": "error", "message": "A conta não pode ser encontrada"})
    return jsonify({"status": "error", "message": "Valor inválido"})

@api_v1.route("/sacar", methods=['PUT'])
@auth.login_required
@permission_required(Permission.USAR)
def sacar():
    dados = request.get_json()
    obrigatorios = ['conta', 'valor']
    
    requisitos(obrigatorios, dados.keys())

    valor = float(dados['valor'])
    if valor > 0:
        conta = Conta.query.filter_by(id=dados['conta'], enabled=True).first()
        if conta:
            if conta.titular_id == g.current_user.id:
                if conta.saldo >= valor:
                    conta.saldo -= valor
                    db.session.add(conta)
                    db.session.commit()

                    return jsonify({"status": "success", "message": "Saque efetuado"})
                
                return jsonify({"status": "error", "message": "Saldo insuficiente"})
            return jsonify({"status": "error", "message": "Não possui autorização para sacar desta conta."})
        return jsonify({"status": "error", "message": "A conta não pode ser encontrada"})
    return jsonify({"status": "error", "message": "Valor inválido"})

@api_v1.route("/transferir", methods=['PUT'])
@auth.login_required
@permission_required(Permission.USAR)
def transferir():
    dados = request.get_json()
    obrigatorios = ['conta_saida', 'conta_entrada', 'valor']
    
    requisitos(obrigatorios, dados.keys())

    conta_saida = Conta.query.filter_by(id=dados['conta_saida'], enabled=True).first()
    conta_entrada = Conta.query.filter_by(id=dados['conta_entrada'], enabled=True).first()
    if conta_saida.titular_id == g.current_user.id:
        return jsonify(Conta.transfere(conta_saida, conta_entrada, dados['valor']))
    return jsonify({"status": "error", "message": "Você não é titular da conta de saída"})
    

    