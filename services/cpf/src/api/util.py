from flask import jsonify


def verify_has_11_digits(cpf):
    if cpf.is_digit():
        return True
    return False


def verify_has_only_digits(cpf):
    return True


def check_cpf_in_serpro(cpf):
    return True