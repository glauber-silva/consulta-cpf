from flask import Blueprint, jsonify

users_blueprint = Blueprint('users', __name__)



@users_blueprint.route('/users/ping', methods=['get'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
