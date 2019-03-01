# services/cpf/src/__init__.py

from flask import Flask, jsonify

app = Flask(__name__)

app.config.from_object('src.config.DevConfig')

@app.route('/cpf/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@app.route("/cpf/<string:cpf>")
def consulta(cpf):
    return 'Cpf consultado: {0}'.format(cpf)