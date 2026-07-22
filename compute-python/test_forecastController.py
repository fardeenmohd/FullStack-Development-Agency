import unittest
from fastapi.testclient import TestClient
from main import app  # Assuming the Flask app is in a file named 'main.py'

class TestForecastController(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_predict_forecast_success(self):
        data = {
            "currency_pairs": ["USD/EUR", "EUR/GBP"],
            "date": "2023-10-01"
        }
        response = self.client.post('/api/v1/forecast/predict', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('predictions', response.json())

    def test_predict_forecast_invalid_data(self):
        data = {
            "currency_pairs": ["USD/EUR", "EUR/GBP"],
            "date": "invalid_date"
        }
        response = self.client.post('/api/v1/forecast/predict', json=data)
        self.assertEqual(response.status_code, 400)

    def test_predict_forecast_missing_data(self):
        data = {
            "currency_pairs": ["USD/EUR", "EUR/GBP"]
        }
        response = self.client.post('/api/v1/forecast/predict', json=data)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
