from flask import Blueprint, jsonify, request

from src.api.models import User
from src.ext.db import db

users_blueprint = Blueprint('users', __name__)



@users_blueprint.route('/users/ping', methods=['get'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route('/users', methods=['post'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    db.session.add(User(username=username, email=email))
    db.session.commit()
    response = {
        'status': 'success',
        'message': f'{email} foi adicionado!'
    }

    return jsonify(response), 201