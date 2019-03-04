from .users import users_blueprint


def init(app):
    app.register_blueprint(users_blueprint)
