from decouple import config

class BaseConfig:
    """Base Config"""
    TESTING = False
    SECRET_KEY = config('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(BaseConfig):
    """Dev configs"""
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config("DATABASE_TEST_URL")


class ProdConfig(BaseConfig):
    """Prod Configs"""
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URL")


