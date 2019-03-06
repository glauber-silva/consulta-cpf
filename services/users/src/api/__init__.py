from .users import users_blueprint
from .auth import auth_blueprint


def init(app):
    app.register_blueprint(users_blueprint)
    app.register_blueprint(auth_blueprint)