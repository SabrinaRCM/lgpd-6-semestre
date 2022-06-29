import json
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


class Permissao(BaseModel):
    id = BigIntegerField(primary_key=True)
    termoAceito = CharField(null=True)

    cliente = ForeignKeyField(Cliente)

    def VerifyPermission(client):
        permission = Permissao.select().join(Cliente).where(Cliente.id == client.id).get()
        var = json.loads(json.dumps(permission.termoAceito))
        itens = json.loads(var.replace("True", "true").replace("False", "false"))
        if "indicacao" in itens["itens"]:
            return itens["itens"]["indicacao"]

    class Meta:
        database = database

    def unauthorizedInfo(listClients):
        convertedLists = []
        convertedNameList = []
        convertedEmailList = []
        convertedPhoneList = []
        convertedCepList = []
        convertedStreetList = []
        for client in listClients:
            anonymous = verifyPermission(client)

            if not anonymous:
                convertedNameList.append(client.nome)
                convertedEmailList.append(client.email)
                convertedPhoneList.append(client.telefone)
                convertedCepList.append(client.cep)
                convertedStreetList.append(client.rua)
            else:
                convertedNameList.append("-")
                convertedEmailList.append("-")
                convertedPhoneList.append("-")
                convertedCepList.append("-")
                convertedStreetList.append("-")

        convertedLists = [
            convertedNameList,
            convertedEmailList,
            convertedPhoneList,
            convertedCepList,
            convertedStreetList,
        ]
        return convertedLists

    def unauthorizedInfo_aberto(listClients, columns):
        convertedLists = []
        sensibleList = verifyIsSensible(columns)
        for column in columns:
            columnSplit = column.split(",")
            listDynamic = globals()[columnSplit[0]] = []

            for client in listClients:
                anonymous = verifyPermission(client)
                dictionary = retriveDictionary(client)

                if (
                    verifyIsMandatory(columnSplit[1])
                    or anonymous
                    and columnSplit[0] in sensibleList
                ):
                    listDynamic.append("-")
                else:
                    listDynamic.append(dictionary[columnSplit[0]])

            convertedLists.append(listDynamic)
        return convertedLists


def verifyIsSensible(columns):
    sensibleList = []
    for column in columns:
        if not int(column.split(",")[1]) > 0:
            sensibleList.append(column.split(",")[0])
    return sensibleList


def verifyIsMandatory(condition):
    if int(condition) > 0:
        return False
    return True


def verifyPermission(client):
    permissions = Permissao.select().join(Cliente).where(Cliente.id == client.id)
    return permissions[0].anonymous


def retriveDictionary(client):
    dictReport = {
        "nome": client.nome,
        "documento": client.documento,
        "email": client.email,
        "cep": client.cep,
        "cidade": client.cidade,
    }
    return dictReport
