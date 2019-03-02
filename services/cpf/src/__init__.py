# services/cpf/src/__init__.py
import os

from flask import Flask, jsonify


app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)


@app.route('/cpf/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@app.route("/cpf/<string:cpf>")
def consulta(cpf):
    return 'Cpf consultado: {0}'.format(cpf)