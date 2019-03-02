from flask import Blueprint, jsonify

cpf_blueprint = Blueprint('cpf', __name__)


@cpf_blueprint.route('/cpf/ping', methods=['get'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })