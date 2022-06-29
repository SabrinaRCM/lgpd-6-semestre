from peewee import *

database = SqliteDatabase("clients.db")


class BaseModel(Model):
    class Meta:
        database = database


class Termo(BaseModel):

    id = BigIntegerField(primary_key=True)
    versao = CharField(null=True)
    itens = CharField(null=True)
    termosUso = CharField(null=True)

    class Meta:
        database = database
