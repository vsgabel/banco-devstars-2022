from flask import current_app, jsonify, request
from app.api.v1 import api_v1
from app.util import Serializer

@api_v1.route("/token", methods=['POST'])
def generate_token():
    dados = request.get_json()
    
    id = dados['id']

    return jsonify({
        "user_id": id,
        "token": Serializer.generate_token(current_app.config['SECRET_KEY'], id)
    })

