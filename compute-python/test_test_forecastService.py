import unittest
from fastapi.testclient import TestClient
from forecast_service import ForecastService

class TestForecastService(unittest.TestCase):

    def setUp(self):
        self.forecast_service = ForecastService()
        self.client = TestClient(self.forecast_service.app)

    def test_get_forecast_valid_location_metric_units(self):
        location = "New York"
        units = "metric"
        expected_result = {"temperature": 10, "condition": "Sunny"}
        response = self.client.get(f"/forecast?location={location}&units={units}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_valid_location_imperial_units(self):
        location = "New York"
        units = "imperial"
        expected_result = {"temperature": 50, "condition": "Sunny"}
        response = self.client.get(f"/forecast?location={location}&units={units}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_invalid_units(self):
        location = "New York"
        units = "invalid"
        expected_result = None
        response = self.client.get(f"/forecast?location={location}&units={units}")
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.json())

    def test_get_forecast_empty_location(self):
        location = ""
        expected_result = None
        response = self.client.get(f"/forecast?location={location}")
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.json())

    def test_get_forecast_invalid_location(self):
        location = "InvalidLocation123"
        expected_result = None
        response = self.client.get(f"/forecast?location={location}")
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.json())

    def test_get_forecast_with_no_units(self):
        location = "New York"
        expected_result = {"temperature": 20, "condition": "Sunny"}
        response = self.client.get(f"/forecast?location={location}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_default_units_metric(self):
        location = "New York"
        expected_result = {"temperature": 10, "condition": "Sunny"}
        response = self.client.get(f"/forecast?location={location}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_default_units_imperial(self):
        location = "Los Angeles"
        expected_result = {"temperature": 50, "condition": "Sunny"}
        response = self.client.get(f"/forecast?location={location}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_custom_temperature_scale_metric(self):
        location = "New York"
        units = "metric"
        temperature_scale = "Celsius"
        expected_result = {"temperature": 10, "condition": "Sunny", "scale": "Celsius"}
        response = self.client.get(f"/forecast?location={location}&units={units}&temperature_scale={temperature_scale}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_custom_temperature_scale_imperial(self):
        location = "New York"
        units = "imperial"
        temperature_scale = "Fahrenheit"
        expected_result = {"temperature": 50, "condition": "Sunny", "scale": "Fahrenheit"}
        response = self.client.get(f"/forecast?location={location}&units={units}&temperature_scale={temperature_scale}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_custom_temperature_scale_invalid(self):
        location = "New York"
        units = "metric"
        temperature_scale = "Kelvin"
        expected_result = None
        response = self.client.get(f"/forecast?location={location}&units={units}&temperature_scale={temperature_scale}")
        self.assertEqual(response.status_code, 400)
        self.assertIsNone(response.json())

    def test_get_forecast_with_missing_temperature(self):
        location = "New York"
        units = "metric"
        expected_result = {"condition": "Sunny"}
        response = self.client.get(f"/forecast?location={location}&units={units}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_missing_condition(self):
        location = "New York"
        units = "metric"
        expected_result = {"temperature": 10}
        response = self.client.get(f"/forecast?location={location}&units={units}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_result)

    def test_get_forecast_with_all_none_values(self):
        location = "InvalidLocation123"
        units = "invalid"
        temperature_scale = "Kelvin"
        expected_result = None
        response = self.client.get(f"/forecast?location={location}&units={units}&temperature_scale={temperature_scale}")
        self.assertEqual(response.status_code, 404)
        self.assertIsNone(response.json())

if __name__ == '__main__':
    unittest.main()
