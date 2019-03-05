import unittest
from flask.cli import FlaskGroup
from src import create_app
from src.ext.db import db
from src.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    """populate db"""
    db.session.add(User(username='teste', email="teste@email.com"))
    db.session.add(User(username="test", email="test@gmail.com"))
    db.session.commit()


@cli.command()
def test():
    """ Runs the tests without coverage"""
    tests = unittest.TestLoader().discover('src/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == '__main__':
    cli()