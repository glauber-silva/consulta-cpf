# services/cpf/src/config.py
from decouple import config

class BaseConfig:
    """Base Config"""
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')

class DevConfig(BaseConfig):
    """Dev configs"""
    pass


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    """Prod Configs"""
    pass

