from faker import Faker
from app import db, login_manager
from datetime import datetime, timedelta
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    USAR = 1
    CRIAR = 2
    ALTERAR_LIMITE = 4
    DESABILITAR = 8
    ADMIN = 16


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128), nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    # modificado_em = db.Column(db.DateTime, nullable=False, onupdate=datetime.now())
    ativo = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    contas = db.relationship('Conta', backref="titular")
    cartoes = db.relationship('Cartao', backref="titular")

    def __init__(self):
        self.criado_em = datetime.now()
        self.modificado_em = datetime.now()
        if not self.role:
            self.role = Role.query.filter_by(padrao=True).first()

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "criado_em": self.criado_em
        }

    @property
    def senha(self):
        raise AttributeError("Este não é um atributo que possa ser lido")

    @senha.setter
    def senha(self, valor):
        self.senha_hash = generate_password_hash(valor)

    def verify_password(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(16), nullable=False)
    perm = db.Column(db.Integer, nullable=False, default=0)
    padrao = db.Column(db.Boolean, default=False, index=True)
    users = db.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        roles = {
            'desabilitado': [],
            'usuario': [Permission.USAR, Permission.CRIAR],
            'funcionario': [Permission.CRIAR, Permission.ALTERAR_LIMITE, Permission.DESABILITAR],
            'admin': [Permission.USAR, Permission.CRIAR, Permission.ALTERAR_LIMITE, Permission.DESABILITAR, Permission.ADMIN]
        }
        padrao = 'usuario'
        for r in roles:
            role = Role.query.filter_by(nome=r).first()
            if not role:
                role = Role()
                role.nome = r
            
            role.reset_permission()
            for perm in roles[r]:
                role.add_permission(perm)
            role.padrao = (role.nome == padrao)
            db.session.add(role)
        db.session.commit()



    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.perm += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.perm -= perm

    def reset_permission(self):
        self.perm = 0

    def has_permission(self, perm):
        return self.perm & perm == perm

class Conta(db.Model):
    __tablename__ = "contas"
    id = db.Column(db.Integer, primary_key=True)
    saldo = db.Column(db.Float)
    enabled = db.Column(db.Boolean, nullable=False, default=True)

    titular_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def transfere(conta_saida, conta_entrada, valor):
        if valor <= 0:
            return {"status": "error", "message": "Valor inválido"}
        
        if conta_saida.saldo < valor:
            return {"status": "error", "message": "Saldo insuficiente"}
        
        if not conta_saida.enabled or not conta_entrada.enabled:
            return {"status": "error", "message": "Uma das contas está desabilitada"}

        if conta_entrada.id == conta_saida.id:
            return {"status": "error", "message": "Transferência entre a mesma conta"}

        conta_saida.saldo -= valor
        conta_entrada.saldo += valor

        db.session.add(conta_saida)
        db.session.add(conta_entrada)
        db.session.commit()

        return {"status": "success", "message": "Operação efetuada com sucesso"}

    def sacar(self, valor):
        if valor > 0:
            if self.saldo >= valor:
                self.saldo -= valor
                db.session.add(self)
                db.session.commit()

                return {"status": "success", "message": "Saque efetuado"}
            return {"status": "error", "message": "Saldo insuficiente"}      
        return {"status": "error", "message": "Valor inválido"}

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            db.session.add(self)
            db.session.commit()

            return {"status": "success", "message": "Depósito efetuado"}
        return {"status": "error", "message": "Valor inválido"}

    def to_dict(self):
        return {
            "id": self.id,
            "saldo": self.saldo,
            "titular": self.titular.nome
        }

class Cartao(db.Model):
    __tablename__ = 'cartoes'
    id = db.Column(db.Integer, primary_key=True)
    bandeira = db.Column(db.String(16))
    numero = db.Column(db.String(64), unique=True)
    cvc = db.Column(db.String(4))
    validade = db.Column(db.Date)
    limite = db.Column(db.Float)
    enabled = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, anos=10):
        f = Faker('pt-BR')
        cartao = f.credit_card_full().split("\n")
        self.validade = datetime.now() + timedelta(days=365*anos)
        self.bandeira = "VISA" if "VISA" in cartao[0] else "JCB" if "JCB" in cartao[0] else cartao[0]
        self.cvc = cartao[3].replace("CVC: ", "").replace("CVV: ", "")
        self.numero = cartao[2].split(" ")[0]

    def __repr__(self):
        return '<Cartão %r>' % self.number

    def verify(self, numero, cvc, validade):
        if self.numero == numero and self.cvc == cvc and self.validade == validade:
            return True
        return False

    def to_dict(self):
        return {
            "bandeira": self.bandeira,
            "numero": self.numero,
            "cvc": self.cvc,
            "validade": self.validade,
            "limite": self.limite
        }