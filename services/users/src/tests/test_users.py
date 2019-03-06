import json
import unittest
from src.tests.base import BaseTestCase
from src.tests.utils import add_user

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
            add_user('glauber', 'glauber@email.com', 'maiorqueoito')
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'glauber',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'teste',
                    'email': 'teste@email.com',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
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
            add_user('glauber', 'glauber@email.com', 'maiorqueoito')
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'glauber',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
            '/users',
            data=json.dumps({}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
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
            add_user('glauber', 'glauber@email.com', 'maiorqueoito')
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'glauber',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'teste2@email.com', 'password': 'maiorqueoito'}),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Dados Inválidos.', data['message'])
            self.assertIn('falha', data['status'])

    def test_add_user_duplicate_email(self):
        """thrown error if the email already exists."""
        with self.client:
            add_user('glauber', 'glauber@email.com', 'maiorqueoito')
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'glauber',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'teste3',
                    'email': 'teste3@email.com',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            response = self.client.post(
                '/users',
                data=json.dumps({
                    'username': 'teste3',
                    'email': 'teste3@email.com',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Este email já esta registrado', data['message'])
            self.assertIn('falha', data['status'])

    def test_add_user_invalid_json_keys_no_password(self):
        """
        Ensure error is thrown if the JSON object
        does not have a password key.
        """
        with self.client:
            add_user('glauber', 'glauber@email.com', 'maiorqueoito')
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'glauber',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='teste',
                    email='teste@email.com')),
                content_type='application/json',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Dados Inválidos.', data['message'])
            self.assertIn('falha', data['status'])


if __name__ == "__main__":
    unittest.main()