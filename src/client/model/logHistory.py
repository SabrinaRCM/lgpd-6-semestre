from peewee import *

from src.client.model.cliente import Cliente

database = SqliteDatabase("clients.db")


class BaseModel(Model):
    class Meta:
        database = database


class LogHistory(BaseModel):

    id = BigIntegerField(primary_key=True)
    acao = CharField(null=True)
    request = CharField(null=True)
    cliente = ForeignKeyField(Cliente)
    date = DateField(null=True)

    class Meta:
        database = database
