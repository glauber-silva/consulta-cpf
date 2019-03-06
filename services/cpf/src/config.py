# services/cpf/src/config.py
import os

from decouple import config

class BaseConfig:
    """Base Config"""
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')
    USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL')

class DevConfig(BaseConfig):
    """Dev configs"""
    pass


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    """Prod Configs"""
    pass

