import unittest

from src.ext.db import db
from src.api.models import User
from src.tests.base import BaseTestCase
from sqlalchemy.exc import IntegrityError


class TestUserModel(BaseTestCase):

    def test_add_user(self):
        user = User(
            username='test',
            email='test@email.com',
        )
        db.session.add(user)
        db.session.commit()
        self.assertTrue(user.id)
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@email.com')
        self.assertTrue(user.active)

    def test_add_user_duplicate_username(self):
        user = User(
            username='test',
            email='test@email.com'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='test',
            email='test@email.com'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)

    def test_add_user_duplicate_email(self):
        user = User(
            username='test',
            email='test@email.com'
        )
        db.session.add(user)
        db.session.commit()
        duplicate_user = User(
            username='othertest',
            email='test@email.com'
        )
        db.session.add(duplicate_user)
        self.assertRaises(IntegrityError, db.session.commit)


if __name__ == '__main__':
    unittest.main()