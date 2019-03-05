import unittest

from src.ext.db import db
from src.api.models import User
from src.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError
from src.tests.utils import add_user

class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = add_user('test', 'test@email.com')
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        add_user('test', 'test@email.com')
        duplicate_user = User(
            username='test',
            email='test2@email.com',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = add_user('test', 'test@email.com')
        duplicate_user = User(
            username='test2',
            email='test@email.com',
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)


if __name__ == '__main__':
    unittest.main()