from flask import Flask
from src.client.model.local import Local
from src.client.model.logHistory import LogHistory

from src.client.controller.clientController import clients_urls_blueprint
from src.client.model.criptografia import Criptografia
from src.client.model.permissao import Permissao
from src.client.model.cliente import Cliente
from src.client.model.termo import Termo
import json

from peewee import *

DATABASE = "clients.db"
DATABASE2 = "criptografia.db"

# Flask App
app = Flask(__name__)
app.register_blueprint(clients_urls_blueprint)

# ORM
database = SqliteDatabase(DATABASE)
database2 = SqliteDatabase(DATABASE2)


def create_tables():
    with database:
        database.create_tables([Cliente, Permissao, Termo, LogHistory, Local])

        loc = Local(nome="+Perto", tipo="Alet", lat="-23.234374678052514", long="-45.88038195171009")
        loc.save()

    termo = Termo(
        versao="1",
        itens=str({"sms": True, "email": False, "telefone": True}).replace("'", '"'),
        termosUso="Termos de uso ipipipipi popopopopop"
    )
    termo.save()

    # objItens = '"versao": 1, "itens": {"sms": true, "email": false, "telefone": true}'

    # perm = Permissao.create(anonymous=False, termoAceito=objItens, cliente=cli)
    # perm.save()
    local = Local.create(nome = "LOCAL", tipo = "BARBEIRO", lat = -23.23534924801826, long = -45.87982800062321)
    local.save()

def create_tables2():
    with database2:
        database2.create_tables([Criptografia])


create_tables()
create_tables2()

if __name__ == "__main__":
    app.run(debug=True)
