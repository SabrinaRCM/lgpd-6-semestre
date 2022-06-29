from src.client.model.termo import Termo
from src.client.model.criptografia import Criptografia
from src.client.model.logHistory import LogHistory
from src.client.model.permissao import Permissao
from src.client.model.cliente import Cliente
from src.client.model.local import Local

from flask import Flask, Blueprint, request
from datetime import datetime
from posixpath import split
import json
import ast

from peewee import *

clients_urls_blueprint = Blueprint(
    "urls_cliente",
    __name__,
)


def getPermission(id):
    return Permissao.select().join(Cliente).where(Cliente.id == id).get()


@clients_urls_blueprint.route("/")
def home():
    # result = select([table.columns.name])
    clis = Cliente.get(Cliente.id == 1)
    print(clis.nome)
    return "OLA"


@clients_urls_blueprint.route("/cadastrar", methods=["POST"])
def cadastrar():

    key = Criptografia.generatekey()

    cli = Cliente(
        nome=request.json["nome"],
        documento=request.json["documento"],
        email=request.json["email"],
        telefone=request.json["telefone"],
        nascimento=request.json["nascimento"],
        cep=request.json["cep"],
        cidade=request.json["cidade"],
        estado=request.json["estado"],
        rua=request.json["rua"],
        bairro=request.json["bairro"],
    )

    cli.nome = Criptografia.encrypt(cli.nome, key)
    cli.documento = Criptografia.encrypt(cli.documento, key)
    cli.email = Criptografia.encrypt(cli.email, key)
    cli.telefone = Criptografia.encrypt(cli.telefone, key)
    cli.save()

    termo = Termo.select().order_by(Termo.id.desc()).get()

    perms = {"versao": termo.versao, "itens": termo.itens}
    perm = Permissao(termoAceito=str(perms).replace("'", '"'), cliente=cli)
    perm.save()

    cript = Criptografia(documento=request.json["documento"], chave=str(key))
    cript.save()
    return "Cadastrado"


@clients_urls_blueprint.route("/alterarPermissao/<int:id>", methods=["POST"])
def alterarPermissao(id):
    storedPerm = getPermission(id)

    if storedPerm:
        perm = Permissao(
            id=storedPerm.id,
            termoAceito=str(request.json).replace("'", '"'),
            cliente=storedPerm.cliente,
        )
        if perm.save():
            LogHistory.create(
                acao="UPD",
                request=request.json,
                cliente=storedPerm.cliente,
                date=datetime.now(),
            )
            return "Atualizado"
    return "Erro"

@clients_urls_blueprint.route("/points", methods=["POST"])
def indicacao():
    lat, long, dist, loggedUser = request.json["lat"], request.json["long"], request.json["maxDistance"], request.json["user"]
    client = Cliente.get(Cliente.id == loggedUser)
    if(not Permissao.VerifyPermission(client)):
        return "Not authorized"
    locations = Local.Distance(lat, long, float(dist))
    
    point = Local.VerifyMoreProximity(locations)
    data = {}
    splittedLocation = point.split("|")
    data["Local"] = splittedLocation[0]
    data["Tipo"] = splittedLocation[1]
    data["Distancia"] = splittedLocation[2]
    recommendationJson = json.dumps(data)

    return recommendationJson
    
@clients_urls_blueprint.route("/sendSMS/<int:id>", methods=["POST"])
def sendSMS(id):
    permission = getPermission(id)
    var = json.loads(json.dumps(permission.termoAceito))
    itens = json.loads(var.replace("True", "true").replace("False", "false"))
    if "sms" in itens["itens"]:
        if not itens["itens"]["sms"]:
            return "Cliente não permite envio de SMS."

    print("Enviando SMS...")
    return "SMS enviado."


@clients_urls_blueprint.route("/sendEmail/<int:id>", methods=["POST"])
def sendEmail(id):
    permission = getPermission(id)
    if permission.email:
        print("Enviando email...")
        return "Email enviado."
    else:
        return "Cliente não permite envio de emails."


@clients_urls_blueprint.route("/visualizar/<id>")
def descriptografar(id):
    cli = Cliente.get(Cliente.id == id)
    nome = cli.nome
    documento = cli.documento
    email = cli.email
    telefone = cli.telefone
    
    chave = Criptografia.get_or_none(id = id)
    if chave == None: 
        return "Cliente não existe!"
    chave = chave.chave
    chave = ast.literal_eval(chave)

    nonce, ciphertext, tag = nome.split("&&")
    nonce, ciphertext, tag = Criptografia.formatCript(nonce, ciphertext, tag)
    cli.nome = Criptografia.decrypt(nonce, ciphertext, tag, chave)

    nonce, ciphertext, tag = documento.split("&&")
    nonce, ciphertext, tag = Criptografia.formatCript(nonce, ciphertext, tag)
    cli.documento = Criptografia.decrypt(nonce, ciphertext, tag, chave)

    nonce, ciphertext, tag = email.split("&&")
    nonce, ciphertext, tag = Criptografia.formatCript(nonce, ciphertext, tag)
    cli.email = Criptografia.decrypt(nonce, ciphertext, tag, chave)

    nonce, ciphertext, tag = telefone.split("&&")
    nonce, ciphertext, tag = Criptografia.formatCript(nonce, ciphertext, tag)
    cli.telefone = Criptografia.decrypt(nonce, ciphertext, tag, chave)

    data = {}
    data["nome"] = cli.nome
    data["documento"] = cli.documento
    data["email"] = cli.email
    data["telefone"] = cli.telefone

    return json.dumps(data)


@clients_urls_blueprint.route("/excluir/<id>")
def excluir(id):
    key = Criptografia.get(Criptografia.id == id)
    key.delete_instance()
    return "Excluido"


@clients_urls_blueprint.route("/relatorio")
def relatorio():
    rows = Cliente.select()
    listClients = list(rows)
    convertedValues = Permissao.unauthorizedInfo(listClients)

    names = convertedValues[0]
    emails = convertedValues[1]
    phones = convertedValues[2]
    ceps = convertedValues[3]
    streets = convertedValues[4]
    districts = [o.bairro for o in listClients]
    citys = [o.cidade for o in listClients]
    state = [o.estado for o in listClients]

    df = pd.DataFrame(
        columns=["Nome", "E-mail", "Telefone", "CEP", "Rua", "Bairro", "Cidade"]
    )
    df = pd.DataFrame(
        {
            "Usuario": names,
            "E-mail": emails,
            "Telefone": phones,
            "CEP": ceps,
            "Rua": streets,
            "Bairro": districts,
            "Cidade": citys,
            "Estado": state,
        }
    )
    df.to_csv("relatorio_clientes_totais.csv")


@clients_urls_blueprint.route("/relatorio_aberto")
def relatorio_aberto():
    lines = []
    with open("column_names.txt") as f:
        columns = f.readlines()

    rows = Cliente.select()
    listClients = list(rows)
    convertedValues = Permissao.unauthorizedInfo_aberto(listClients, columns)

    df = pd.DataFrame()
    i = 0
    while i <= len(columns) - 1:
        df[columns[i].split(",")[0]] = convertedValues[i]
        i = i + 1

    df.to_csv("relatorio_clientes_aberto.csv")
    return "ok"
