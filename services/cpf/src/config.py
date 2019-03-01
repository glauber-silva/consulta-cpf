# services/cpf/project/config.py

class BaseConfig:
    """Base Config"""
    TESTING = False


class DevConfig(BaseConfig):
    """Dev configs"""
    pass


class TestConfig(BaseConfig):
    TESTING = True


class ProdConfig(BaseConfig):
    """Prod Configs"""
    pass

