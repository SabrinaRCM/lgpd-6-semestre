from peewee import *
from Crypto.Cipher import AES
from secrets import token_bytes
import ast

database = SqliteDatabase("criptografia.db")


class BaseModel(Model):
    class Meta:
        database = database


class Criptografia(BaseModel):

    id = BigIntegerField(primary_key=True)
    documento = CharField(null=True)
    chave = CharField(null=True)

    class Meta:
        database = database

    def generatekey(): 
        key = token_bytes(32)
        return key

    def encrypt(msg, key):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(msg.encode())
        return """{}&&{}&&{}""".format(nonce, ciphertext, tag)

    def decrypt(nonce, ciphertext, tag, key):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            return plaintext.decode()
        except:
            return False

    def formatCript(nonce, ciphertext, tag):
        nonce = ast.literal_eval(nonce)
        ciphertext = ast.literal_eval(ciphertext)
        tag = ast.literal_eval(tag)
        return nonce, ciphertext, tag

    # def formatDecrypt(nonce, ciphertext, tag, campo, lista = []): 
    #     nonce, ciphertext, tag = campo.split(",")
    #     nonce, ciphertext, tag, chave = Criptografia.format(nonce, ciphertext, tag, chave)
    #     lista = Criptografia.decrypt(nonce, ciphertext, tag, chave)

    # def retriveDictionary(client):
    #     dictReport = {
    #         "nome": client.nome, 
    #         "documento": client.documento, 
    #         "email": client.email, 
    #         "telefone": client.telefone, 
    #         "nascimento": client.nascimento,
    #         "cep": client.cep,
    #         "cidade": client.cidade,
    #         "estado": client.estado,
    #         "rua": client.rua,
    #         "bairro": client.bairro
    #         }
    #     return dictReport