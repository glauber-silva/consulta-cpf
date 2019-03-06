from enum import Enum
import json
from functools import wraps

import requests
from flask import jsonify, current_app, request
from decouple import config


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = {
            'status': 'error',
            'message': 'Alguma coisa deu errado, Contate-nos.'
        }
        code = 401
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            response['message'] = 'Forneça um token válido.'
            code = 403
            return jsonify(response), code
        auth_token = auth_header.split(' ')[1]
        resp = ensure_authentication(auth_token)
        if not resp:
            response['message']= "Token inválido."
            return jsonify(response), code
        return f(response, *args, **kwargs)
    return decorated_function


def ensure_authentication(token):
    url = '{0}/auth/status'.format(current_app.config['USERS_SERVICE_URL'])
    bearer = 'Bearer {0}'.format(token)
    headers = {'Authorization': bearer}
    resp = requests.get(url, headers=headers)
    data = json.loads(resp.text)
    if resp.status_code == 200 and \
        data['status'] == 'success' and \
        data['data']['active']:
        return data
    else:
        return False


def verify_has_11_digits(cpf):
    if len(cpf) != 11:
        return False
    return True


def verify_has_only_digits(cpf):
    if cpf.isdigit():
        return True
    return False


def check_cpf_in_serpro(cpf):
    api_token = config('SERPRO_TOKEN')
    api_url_base = config("SERPRO_URL") + cpf
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {0}'.format(api_token)
    }
    r = requests.get(api_url_base, headers=headers)

    return r.json()


STATUS_LIST = {
    "0": "regular",
    "2": "suspenso",
    "3": "falecido",
    "4": "irregular",
    "5": "cancelado",
    "8": "nulo",
    "9": "cancelado"
}

SERPRO_CODES = ["0","2", "3", "4", "5", "8", "9"]