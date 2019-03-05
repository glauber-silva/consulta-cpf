import os

from flask import Flask
from src.api import init as init_users
from src.ext.db import db
from src.api.models import User

def create_app(sript_info=None):

    # instantiate app
    app = Flask(__name__)

    # config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # extensions
    db.init_app(app)

    # blueprints
    init_users(app)

    # shell context for cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}

    return app
