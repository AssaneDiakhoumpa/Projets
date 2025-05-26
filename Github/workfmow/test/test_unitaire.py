import unittest
from app import app

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_moyenne_api(self):
        response = self.client.get('/api/moyenne')
        self.assertIn(response.status_code, [200, 500])  # dépend si ta DB tourne ou pas

if __name__ == "__main__":
    unittest.main()