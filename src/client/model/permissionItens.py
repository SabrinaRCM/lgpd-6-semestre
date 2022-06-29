from time import sleep
from peewee import *
from .cliente import Cliente

database = SqliteDatabase("clients.db")


class BaseModel(Model):
    class Meta:
        database = database


class IsMandatory:
    Mandatory = (0,)
    NotMandatory = 1


class PermissionItens(BaseModel):
    id = BigIntegerField(primary_key=True)
    version = BigIntegerField(primary_key=True)
    itens = CharField(null=True)

def retriveDictionary(client):
    dictReport = {
        "nome": client.nome,
        "version": client.version,
        "itens": client.itens,
    }
    return dictReport
