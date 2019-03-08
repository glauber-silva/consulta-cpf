from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from src.api.models import User
from src.ext.db import db, bcrypt
from src.api.utils import authenticate

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    """
    Get post data and register user
    """
    data = request.get_json()
    resp = {
        'status': 'falha',
        'message': 'Dados inválidos.'
    }

    if not data:
        return jsonify(resp), 400
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    try:
        # check if user exist
        user_by_name = User.query.filter_by(username=username).first()
        user_by_email = User.query.filter_by(email=email).first()
        if not user_by_name and not user_by_email:
            # add new user
            newuser = User(
                username=username,
                email=email,
                password=password
            )
            db.session.add(newuser)
            db.session.commit()

            # generate a token
            auth_token = newuser.encode_auth_token(newuser.id)
            resp['status'] = 'success'
            resp['message'] = 'Registrado com sucesso.'
            resp['auth_token'] = auth_token.decode()
            return jsonify(resp), 201
        else:
            resp['message'] = 'Usuário existente'
            return jsonify(resp), 400

        # errors
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(resp), 400

@auth_blueprint.route('/auth/login', methods=['post'])
def login_user():
    # get post data
    data = request.get_json()
    resp = {
        'status': 'falha',
        'message': 'Dados inválidos.'
    }

    if not data:
        return jsonify(resp),400
    username = data.get('username')
    password = data.get('password')
    try:
        # fetch user data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                resp['status'] = 'success'
                resp['message'] = 'Login realizado com sucesso.'
                resp['auth_token'] = auth_token.decode()
                return jsonify(resp), 200
        else:
            resp['message'] = 'Usuário não existe.'
            return jsonify(resp), 404
    except Exception:
        resp['message'] = 'Tente outra vez.'
        return jsonify('resp'), 500


@auth_blueprint.route('/auth/logout', methods=['get'])
@authenticate
def logout_user(resp):
    # get auth token
    response = {
        'status': 'success',
        'message': 'Desconectado com sucesso.'
    }
    return jsonify(response), 200


@auth_blueprint.route('/auth/status', methods=['get'])
@authenticate
def get_user_status(resp):
    # user = User.query.filter_by(id=resp).first()
    response = {
        'status': 'success',
        'message': 'Sucesso.',
        'data': resp['user']
    }
    return jsonify(response), 200