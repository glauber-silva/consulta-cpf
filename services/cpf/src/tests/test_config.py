import os
import unittest

from decouple import config
from flask import current_app
from flask_testing import TestCase

from src import create_app

app = create_app()


class TestDevConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.DevConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == config("SECRET_KEY"))
        self.assertFalse(current_app is None)


class TestTestConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['SECRET_KEY'] == config("SECRET_KEY"))
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])


class TestProdConfig(TestCase):
    def create_app(self):
        app.config.from_object('src.config.ProdConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['SECRET_KEY'] == config("SECRET_KEY"))
        self.assertFalse(app.config['TESTING'])


if __name__ == '__main__':
    unittest.main()