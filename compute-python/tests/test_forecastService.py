import unittest
from forecast_service import ForecastService

class TestForecastService(unittest.TestCase):

    def setUp(self):
        self.forecast_service = ForecastService()

    def test_get_forecast_valid_location_metric_units(self):
        location = "New York"
        units = "metric"
        expected_result = {"temperature": 10, "condition": "Sunny"}
        result = self.forecast_service.get_forecast(location, units=units)
        self.assertEqual(result, expected_result)

    def test_get_forecast_valid_location_imperial_units(self):
        location = "New York"
        units = "imperial"
        expected_result = {"temperature": 50, "condition": "Sunny"}
        result = self.forecast_service.get_forecast(location, units=units)
        self.assertEqual(result, expected_result)

    def test_get_forecast_invalid_units(self):
        location = "New York"
        units = "invalid"
        expected_result = None
        result = self.forecast_service.get_forecast(location, units=units)
        self.assertEqual(result, expected_result)

    def test_get_forecast_empty_location(self):
        location = ""
        expected_result = None
        result = self.forecast_service.get_forecast(location)
        self.assertEqual(result, expected_result)

    def test_get_forecast_invalid_location(self):
        location = "InvalidLocation123"
        expected_result = None
        result = self.forecast_service.get_forecast(location)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_no_units(self):
        location = "New York"
        expected_result = {"temperature": 20, "condition": "Sunny"}
        result = self.forecast_service.get_forecast(location)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_default_units_metric(self):
        location = "New York"
        expected_result = {"temperature": 10, "condition": "Sunny"}
        result = self.forecast_service.get_forecast(location)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_default_units_imperial(self):
        location = "Los Angeles"
        expected_result = {"temperature": 50, "condition": "Sunny"}
        result = self.forecast_service.get_forecast(location)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_custom_temperature_scale_metric(self):
        location = "New York"
        units = "metric"
        temperature_scale = "Celsius"
        expected_result = {"temperature": 10, "condition": "Sunny", "scale": "Celsius"}
        result = self.forecast_service.get_forecast(location, units=units, temperature_scale=temperature_scale)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_custom_temperature_scale_imperial(self):
        location = "New York"
        units = "imperial"
        temperature_scale = "Fahrenheit"
        expected_result = {"temperature": 50, "condition": "Sunny", "scale": "Fahrenheit"}
        result = self.forecast_service.get_forecast(location, units=units, temperature_scale=temperature_scale)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_custom_temperature_scale_invalid(self):
        location = "New York"
        units = "metric"
        temperature_scale = "Kelvin"
        expected_result = None
        result = self.forecast_service.get_forecast(location, units=units, temperature_scale=temperature_scale)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_missing_temperature(self):
        location = "New York"
        units = "metric"
        expected_result = {"condition": "Sunny"}
        result = self.forecast_service.get_forecast(location, units=units)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_missing_condition(self):
        location = "New York"
        units = "metric"
        expected_result = {"temperature": 10}
        result = self.forecast_service.get_forecast(location, units=units)
        self.assertEqual(result, expected_result)

    def test_get_forecast_with_all_none_values(self):
        location = "InvalidLocation123"
        units = "invalid"
        temperature_scale = "Kelvin"
        expected_result = None
        result = self.forecast_service.get_forecast(location, units=units, temperature_scale=temperature_scale)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
