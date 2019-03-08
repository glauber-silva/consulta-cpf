# services/cpf/src/__init__.py
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from src.api import init as init_cpf

app = Flask(__name__)
file_handler = RotatingFileHandler("cpf.log", maxBytes=10000, backupCount=3)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

def create_app(sript_info=None):

    # instantiate app
    _app = app

    # config
    app_settings = os.getenv('APP_SETTINGS')
    # app_settings = config('APP_SETTINGS')
    app.config.from_object(app_settings)

    # extensions

    # blueprints
    # from src.api.cpf import cpf_blueprint
    # app.register_blueprint(cpf_blueprint)
    init_cpf(_app)

    # shell context for cli
    @app.shell_context_processor
    def ctx():
        return {'app': _app}


    return _app