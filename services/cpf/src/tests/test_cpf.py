import json
import unittest
from src.tests.base import BaseTestCase


class TestCpfService(BaseTestCase):
    """Tests for the CPF Service"""

    def test_cpf(self):
        """checks if the route / ping (to check sanity) works correctly."""
        response = self.client.get("/cpf/ping")
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])


if __name__ == "__main__":
    unittest.main()
