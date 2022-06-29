from peewee import *

database = SqliteDatabase("clients.db")

class BaseModel(Model):
    class Meta:
        database = database


class Cliente(BaseModel):

    id = BigIntegerField(primary_key=True)
    nome = CharField(null=True)
    email = CharField(null=True)
    telefone = CharField(null=True)
    documento = CharField(null=True)
    nascimento = DateField(null=True)

    cep = CharField(null=True)
    cidade = CharField(null=True)
    estado = CharField(null=True)
    bairro = CharField(null=True)
    rua = CharField(null=True)
    numero = CharField(null=True)
    complemento = CharField(null=True)

    # def __init__(self, name, document):
    #     self.name = name
    #     self.document = document

    # def encrypt():
    #     print("Cript data")

    class Meta:
        database = database