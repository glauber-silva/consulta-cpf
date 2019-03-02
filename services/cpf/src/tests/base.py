from flask_testing import TestCase
from src import create_app

app = create_app()

class BaseTestCase(TestCase):
    def create_app(self):
        app.config.from_object('src.config.TestConfig')
        return app
