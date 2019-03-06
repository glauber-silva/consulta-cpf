from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from src.api.models import User
from src.ext.db import db, bcrypt


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
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
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
def logout_user():
    # get auth token
    auth_header = request.headers.get('Authorization')
    resp = {
        'status': 'falha',
        'message': 'Forneça o token válido'
    }
    if auth_header:
        auth_token = auth_header.split(' ')[1]
        resp_token = User.decode_auth_token(auth_token)
        if not isinstance(resp_token, str):
            resp['status'] = 'success'
            resp['message'] = 'Desconectado com sucesso.'
            return jsonify(resp), 200
        else:
            resp['message'] = resp
            return jsonify(resp), 401
    else:
        return jsonify(resp), 403