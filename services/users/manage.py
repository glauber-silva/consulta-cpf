import unittest

import coverage
from flask.cli import FlaskGroup
from src import create_app
from src.ext.db import db
from src.api.models import User

COV = coverage.coverage(
    branch=True,
    include='src/*',
    omit=[
        'src/tests/*',
        'src/config.py'
    ]
)

COV.start()

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
    db.session.add(User(username='teste', email="teste@email.com", password="maiorqueoito"))
    db.session.add(User(username="test", email="test@email.com", password="maiorqueoito"))
    db.session.commit()

@cli.command()
def cov():
    """ Run unit tests with coverage """
    tests = unittest.TestLoader().discover('src/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print("Coverage Summary: ")
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

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