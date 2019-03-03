import json
import unittest
from src.tests.base import BaseTestCase


class TestCpfService(BaseTestCase):
    """Tests for the CPF Service"""

    def test_cpf_ping(self):
        """checks if the route / ping (to check sanity) works correctly."""
        response = self.client.get("/cpf/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_get_cpf_situation(self):
        """
        Get cpf situation
        """
        cpf = '40442820135'
        with self.client:
            response = self.client.get('/cpf/{cpf}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn("regular", data["status"])

    def test_cpf_is_digit(self):
        """
        CPF must only accept digits
       """
        cpf = 'ABCD5678901'
        with self.client:
            response = self.client.get('/cpf/{cpf}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('CPF Inválido, deve conter somente números', data['error']['reason'])

    def test_cpf_has_11_digits(self):
        """
        CPF must have 11 digits
        """
        cpf = '5678901'
        with self.client:
            response = self.client.get('/cpf/{cpf}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('CPF Inválido, deve conter 11 digitos', data['error']['reason'])

    def test_cpf_is_not_empty(self):
        """
        CPF must be not empty
        """
        cpf = ''
        with self.client:
            response = self.client.get('/cpf/{cpf}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('CPF Inválido, deve conter 11 digitos', data['error']['reason'])

if __name__ == "__main__":
    unittest.main()
