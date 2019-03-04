# services/cpf/src/__init__.py
import os

from decouple import config
from flask import Flask
from src.api import init as init_cpf


def create_app(sript_info=None):

    # instantiate app
    app = Flask(__name__)

    # config
    app_settings = os.getenv('APP_SETTINGS')
    # app_settings = config('APP_SETTINGS')
    app.config.from_object(app_settings)

    # extensions

    # blueprints
    # from src.api.cpf import cpf_blueprint
    # app.register_blueprint(cpf_blueprint)
    init_cpf(app)

    # shell context for cli
    @app.shell_context_processor
    def ctx():
        return {'app': app}

    return app