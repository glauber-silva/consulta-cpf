import json
import unittest
from src.tests.base import BaseTestCase


class TestUsersService(BaseTestCase):
    """Tests for the USERS Service"""

    def test_users_ping(self):
        """checks if the route /ping (to check sanity) works correctly."""
        response = self.client.get("/users/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'teste',
                    'email': 'teste@email.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('teste@email.com foi adicionado!', data['message'])
            self.assertIn('success', data['status'])


    def test_add_user_invalid_json(self):
        """
        thrown a error if JSON is invalid
        """
        with self.client:
            response = self.client.post(
            '/users',
            data=json.dumps({}),
            content_type='application/json',
        )

        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Dados Inválidos.', data['message'])
        self.assertIn('falha', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        thrown a error if JSON does not have username
        """
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'teste2@email.com'}),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Dados Inválidos.', data['message'])
            self.assertIn('falha', data['status'])

    def test_add_user_duplicate_email(self):
        """thrown error if the email already exists."""
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'teste3',
                    'email': 'teste3@email.com'
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'teste3',
                    'email': 'teste3@email.com'
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Este email já existe', data['message'])
            self.assertIn('falha', data['status'])


if __name__ == "__main__":
    unittest.main()