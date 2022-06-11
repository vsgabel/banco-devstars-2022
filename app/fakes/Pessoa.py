from faker import Faker
from random import randint
import requests

class Pessoa:
    def __init__(self) -> None:
        f = Faker('pt-BR')

        self.nome = f.name()
        self.cpf = f.ssn()
        self.email = self.nome.replace(".", "").replace(" ","").lower()+"@gmail.com"
        self.senha = str(randint(1000,99999))

        completo = f.address().split("\n")
        loc, estado = completo[2].split(" / ")
        resto = loc.split(" ")

        if ',' in completo:
            temp = completo[0].split(',')
            self.endereco = temp[0]
            self.numero = temp[1]
            # self.endereco, self.numero = completo[0].split(',')
        else:
            self.endereco = completo[0]
            self.numero = None

        # self.endereco, self.numero = completo[0].split(',') if ',' in completo else [completo[0], None]
        self.bairro = completo[1]
        self.cep = resto.pop(0).replace("-", "")
        while len(self.cep) < 8:
            self.cep = "0" + self.cep
        self.cidade = ' '.join(resto)
        self.estado = estado
        self.nascimento = f.date()

    def to_dict(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "senha": self.senha,
            "endereco": self.endereco,
            "numero": self.numero,
            "bairro": self.bairro,
            "cep": self.cep,
            "cidade": self.cidade,
            "estado": self.estado,
            "nascimento": self.nascimento,
        }

def popula_db(n):
    for _ in range(n):
        resp = requests.post("http://localhost:5000/api/v1/usuario", json=Pessoa().to_dict())
        print(resp.status_code)