import unittest

from src.ext.db import db
from src.api.models import User
from src.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from src.tests.utils import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('test', 'test@email.com', 'maiorqueoito')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('test', 'test@email.com', 'maiorqueoito')
        duplicate_user = User(
            username='test',
            email='test2@email.com',
            password='maiorqueoito',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user('test', 'test@email.com', 'maiorqueoito')
        duplicate_user = User(
            username='test2',
            email='test@email.com',
            password='maiorqueoito',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_passwords_are_random(self):
        user_one = add_user('test', 'test@email.com', 'maiorqueoito')
        user_two = add_user('test2', 'test2@email.com', 'maiorqueoito')
        self.assertNotEqual(user_one.password, user_two.password)

if __name__ == '__main__':
    unittest.main()