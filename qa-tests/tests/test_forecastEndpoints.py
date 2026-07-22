import requests
import unittest

class TestForecastEndpoints(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://localhost:5000/api/forecast"

    def test_get_forecast_success(self):
        response = self._get_forecast("New York")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("temperature", data)
        self.assertIn("humidity", data)

    def test_get_forecast_failure(self):
        response = self._get_forecast("InvalidCity")
        self.assertEqual(response.status_code, 404)

    def _test_fetch_forecast_with_token(self, token, expected_status_code):
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.get(f"{self.base_url}/city?name=New York", headers=headers)
        self.assertEqual(response.status_code, expected_status_code)
        if expected_status_code == 200:
            data = response.json()
            self.assertIn("temperature", data)
            self.assertIn("humidity", data)

    def test_fetch_forecast_with_valid_token_success(self):
        self._test_fetch_forecast_with_token("valid_token", 200)

    def test_fetch_forecast_with_invalid_token_failure(self):
        self._test_fetch_forecast_with_token("invalid_token", 401)

    def test_fetch_forecast_with_no_token_failure(self):
        response = requests.get(f"{self.base_url}/city?name=New York")
        self.assertEqual(response.status_code, 401)

if __name__ == "__main__":
    unittest.main()
