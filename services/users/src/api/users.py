from flask import Blueprint, jsonify, request

from sqlalchemy import exc
from src.api.models import User
from src.ext.db import db
from src.api.utils import authenticate

users_blueprint = Blueprint('users', __name__)



@users_blueprint.route('/users/ping', methods=['get'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['post'])
@authenticate
def add_user(resp):
    data = request.get_json()
    resp = {
        "status": "falha",
        "message": "Dados Inválidos."
    }
    if not data:
        return jsonify(resp), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()
            resp['status'] = 'success'
            resp['message'] = f'{email} foi adicionado!'
            return jsonify(resp), 201
        else:
            resp['message'] = 'Este email já esta registrado'
            return jsonify(resp), 400
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(resp), 400
