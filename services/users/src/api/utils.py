from functools import wraps

from flask import request, jsonify
from src.api.models import User


def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        resp = {
            'status': 'falha',
            'message': 'Forneça um token válido.'
        }
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify(resp), 403
        auth_token = auth_header.split(" ")[1]
        resp_token = User.decode_auth_token(auth_token)
        if isinstance(resp_token, str):
            resp['message'] = resp_token
            return jsonify(resp), 401
        user = User.query.filter_by(id=resp_token).first()
        if not user or not user.active:
            return jsonify(resp), 401
        return f(resp, *args, **kwargs)

    return decorated_function