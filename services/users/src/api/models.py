import datetime

import jwt
from flask import current_app
from sqlalchemy.sql import func
from src.ext.db import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()

    def encode_auth_token(self, user_id):
        """
        Will generate a auth token
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get("SECRET_KEY"),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        decodes the auth token
        :param auth_token:
        :return: integer | string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expiradao. Faça um novo login, por favor.'
        except jwt.InvalidTokenError:
            return "Token Inválido. Faça um novo login, por favor."
