# services/cpf/src/config.py


class BaseConfig:
    """Base Config"""
    TESTING = False
    SECRET_KEY = 'somegreatstringhere20199102'

class DevConfig(BaseConfig):
    """Dev configs"""
    pass


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    """Prod Configs"""
    pass

