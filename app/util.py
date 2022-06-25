import jwt
import datetime
import time
from app.models import User

def requisitos(campos, chaves):
    falta = []

    for campo in campos:
        if campo not in chaves:
            falta.append(campo)        
    
    if falta:
        abort(422, f"O(s) campo(s) {falta} é(são) obrigatório(s)")

class Serializer:
    '''
    Baseado no código de Robin Uphoff, obtido em 15 de junho de 2022
    Classe estática com dois métodos para geração de um token e sua confirmação utilizando
    a biblioteca PyJWT. Para instalar este requisito:
    pip install pyjwt
    Referências:
    https://stackoverflow.com/questions/71292764/which-timed-jsonwebsignature-serializer-replacement-for-itsdangerous-is-better
    '''
    @staticmethod
    def generate_token(secret_key:str, user_id:int, expiration=86400):
        '''
        Gera um token de confirmação com a id do usuário e uma expiração.
        Recebe como retorno um token de 121 caracteres.
        secret_key: str, chave utilizada nas configurações do app
        user_id: int, id do usuário que será confirmada
        expiration: int, número de segundos para expirar o token
        (str, int, int) -> str
        '''
        token = jwt.encode(
            {
                "confirm": user_id,
                "exp": datetime.datetime.now(tz=datetime.timezone.utc)
                       + datetime.timedelta(seconds=expiration)
            },
            secret_key,
            algorithm="HS256"
        )
        return token

    @staticmethod
    def confirm(secret_key:str, user_id:int, token:str, treshold=10):
        '''
        Confirma o token gerado pelo método generate_token,
        considerando treshold segundos de tolerância.
        secret_key: str, chave utilizada nas configurações do app
        user_id: int, id do usuário logado
        token: str, token gerado anteriormente
        treshold: int, segundos de tolerância para a validação da chave
        (str, int, str, int) -> bool
        '''
        try:
            data = jwt.decode(
                token,
                secret_key,
                leeway=datetime.timedelta(seconds=treshold),
                algorithms=["HS256"]
            )
        except:
            return False

        if data.get('confirm') != user_id:
            return False
        return True

    @staticmethod
    def verify_auth_token(secret_key, token, treshold=10):
        data = jwt.decode(
                token,
                secret_key,
                leeway=datetime.timedelta(seconds=treshold),
                algorithms=["HS256"]
            )
        return User.query.get(data['confirm'])

    @classmethod
    def test(cls, sleep=1, treshold=10, expiration=10):
        '''
        Método de teste do funcionamento desta classe. Gera um token, e mostra
        na tela o tempo decorrido até sua expiração.
        sleep: int, tempo de espera (em segundos) entre os testes
        treshold: int, tolerância (em segundos) para a expiração
        expiration: int, tempo para expiração (em segundos) do token
        (int, int, int) -> None
        '''
        token = cls.generate_token("kkk", 1, expiration=expiration)
        print(f"TOKEN: {token}\n")
        t = 0
        while t <= expiration + treshold + 1:
            print(f"t = {t} s: {cls.confirm('kkk', 1, token)}")
            time.sleep(sleep)
            t += sleep