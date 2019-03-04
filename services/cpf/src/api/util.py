from enum import Enum

import requests
from flask import jsonify
from decouple import config


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