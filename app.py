from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Olá Mundo"

@app.route("/consulta/<string:cpf>")
def consulta(cpf):
    return 'Cpf consultado: {0}'.format(cpf)