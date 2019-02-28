import os

class BaseConfig(object):
    """Main configuration"""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenvb('SECRET')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevConfig(BaseConfig):
    """Configs for Development"""
    DEBUG = True


class TestConfig(Config):
    """ Configs for test """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/consultacpf_test'
    DEBUG = True


class StaginConfig(Config):
    """Configs for Staging"""
    DEBUG = False


class ProdConfig(Config):
    """Configs for Staging"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevConfig,
    'testing': TestConfig,
    'stagin': StaginConfig,
    'production': ProdConfig
}