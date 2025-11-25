
import os
import unittest
from unittest.mock import patch, MagicMock
import sys

# Mocking controllers to avoid import errors if dependencies are missing or side effects occur
sys.modules['controllers'] = MagicMock()
sys.modules['controllers.mainprices'] = MagicMock()
sys.modules['controllers.genai'] = MagicMock()
sys.modules['controllers.brapi'] = MagicMock()

# Set API KEY before importing api
os.environ['API_KEY'] = 'test-secret-key'

from api import api

class TestApiKeyAuth(unittest.TestCase):
    def setUp(self):
        self.app = api.test_client()
        self.app.testing = True

    def test_missing_api_key(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)

    def test_invalid_api_key(self):
        response = self.app.get('/', headers={'X-API-Key': 'wrong-key'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized', response.data)

    def test_valid_api_key(self):
        # We need to mock the view function return value because we mocked the controllers
        # But wait, the view function in api.py returns a dict directly for '/' route.
        # For other routes it calls controllers.
        # Let's test '/' which is self-contained in api.py (mostly)
        # Actually '/' returns a dict.
        response = self.app.get('/', headers={'X-API-Key': 'test-secret-key'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
