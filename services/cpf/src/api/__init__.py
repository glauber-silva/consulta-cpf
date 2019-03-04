from .cpf import cpf_blueprint


def init(app):
    app.register_blueprint(cpf_blueprint)
