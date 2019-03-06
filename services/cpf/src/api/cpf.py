from flask import Blueprint, jsonify
from .util import verify_has_only_digits, verify_has_11_digits, check_cpf_in_serpro, STATUS_LIST, SERPRO_CODES, \
    authenticate

cpf_blueprint = Blueprint('cpf', __name__)


@cpf_blueprint.route('/cpf/ping', methods=['get'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@cpf_blueprint.route('/cpf/', methods=['get'])
@authenticate
def root_route():
    return jsonify({
            "error": {
                "reason": "CPF Inválido. Um CPF válido deve conter 11 digitos numéricos"
            }
        }), 404


@cpf_blueprint.route('/cpf/<cpf>', methods=['get'])
@authenticate
def check_cpf(cpf):
    """
    check cpf
    https://apigateway.serpro.gov.br/consulta-cpf-trial/v1/cpf/{cpf}
    """
    response_object = {}

    try:
        if verify_has_11_digits(cpf) and verify_has_only_digits(cpf):
            resp = check_cpf_in_serpro(cpf)
            if resp["situacao"]["codigo"] in SERPRO_CODES:
                response_object["status"] = STATUS_LIST[resp["situacao"]["codigo"]]
                return jsonify(response_object), 200
            else:
                response_object = {
                    "error": {
                        "reason": resp
                    }
                }
                return jsonify(response_object), 404
        else:
            response_object = {
                "error": {
                    "reason": "CPF Inválido. Um CPF válido deve conter 11 digitos numéricos"
                }
            }
            return jsonify(response_object), 404

    except ValueError:
        response_object = {
            "error": {
                "reason": "CPF Inválido. Um CPF válido deve conter 11 digitos numéricos"
            }
        }

        return jsonify(response_object), 404
