import json
import unittest

from src.api.models import User
from src.tests.base import BaseTestCase
from src.tests.utils import add_user


class TestAuthBlueprint(BaseTestCase):

    def test_user_registration(self):
        with self.client:
            resp = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test',
                    'email': 'test@email.com',
                    'password': 'maiorqueoito',
                }),
                content_type='application/json'
            )
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Registrado com sucesso.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(resp.content_type == 'application/json')
            self.assertEqual(resp.status_code, 201)

    def test_user_registration_duplicate_username(self):
        add_user('test', 'test@email.com', 'maiorqueoito')
        with self.client:
            resp = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test',
                    'email': 'test2@email.com',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json',
            )
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 400)
            self.assertIn(
                'Usuário existente', data['message'])
            self.assertIn('falha', data['status'])

    def test_user_registration_invalid_json(self):
        with self.client:
            resp = self.client.post(
                '/auth/register',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 400)
            self.assertIn('Dados inválidos.', data['message'])
            self.assertIn('falha', data['status'])

    def test_user_registration_invalid_json_keys_no_username(self):
        with self.client:
            resp = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'email': 'teste@email.com',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json',
            )
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 400)
            self.assertIn('Dados inválidos.', data['message'])
            self.assertIn('falha', data['status'])

    def test_user_registration_invalid_json_keys_no_email(self):
        with self.client:
            resp = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json',
            )
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 400)
            self.assertIn('Dados inválidos.', data['message'])
            self.assertIn('falha', data['status'])

    def test_user_registration_invalid_json_keys_no_password(self):
        with self.client:
            resp = self.client.post(
                '/auth/register',
                data=json.dumps({
                    'username': 'test',
                    'email': 'teste@email.com'
                }),
                content_type='application/json',
            )
            data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 400)
            self.assertIn('Dados inválidos', data['message'])
            self.assertIn('falha', data['status'])

    def test_registered_user_login(self):
        with self.client:
            add_user('test', 'test@email.com', 'maiorqueoito')
            resp = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Login realizado com sucesso.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(resp.content_type == 'application/json')
            self.assertEqual(resp.status_code, 200)

    def test_not_registered_user_login(self):
        with self.client:
            resp = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'falha')
            self.assertTrue(data['message'] == 'Usuário não existe.')
            self.assertTrue(resp.content_type == 'application/json')
            self.assertEqual(resp.status_code, 404)


    def test_valid_logout(self):
        add_user('test', 'test@email.com', 'maiorqueoito')
        with self.client:
            # user login
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            # valid token logout
            token = json.loads(resp_login.data.decode())['auth_token']
            resp = self.client.get(
                '/auth/logout',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Desconectado com sucesso.')
            self.assertEqual(resp.status_code, 200)

    def test_user_status(self):
        add_user('test', 'test@email.com', 'maiorqueoito')
        with self.client:
            resp_login = self.client.post(
                '/auth/login',
                data=json.dumps({
                    'username': 'test',
                    'password': 'maiorqueoito'
                }),
                content_type='application/json'
            )
            token = json.loads(resp_login.data.decode())['auth_token']
            response = self.client.get(
                '/auth/status',
                headers={'Authorization': f'Bearer {token}'}
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['username'] == 'test')
            self.assertTrue(data['data']['email'] == 'test@email.com')
            self.assertTrue(data['data']['active'] is True)
            self.assertEqual(response.status_code, 200)

    def test_invalid_status(self):
        with self.client:
            resp = self.client.get(
                '/auth/status',
                headers={'Authorization': 'Bearer invalid'})
            data = json.loads(resp.data.decode())
            self.assertTrue(data['status'] == 'falha')
            self.assertTrue(
                data['message'] == 'Token Inválido. Faça um novo login, por favor.')
            self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()