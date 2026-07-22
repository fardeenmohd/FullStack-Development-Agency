import unittest
from flask import Flask
from forecastEndpoints import forecast_bp, Forecast

class TestForecastEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(forecast_bp)
        self.client = self.app.test_client()
        
        # Mock the Forecast model query methods
        Forecast.query.filter_by.return_value.all.side_effect = [
            [{'id': 1, 'type': 'historical', 'data': 'Historical Data'}],
            [{'id': 2, 'type': 'trend', 'data': 'Market Trends'}],
            [{'id': 3, 'type': 'conversion_rate', 'data': 'Lead Conversion Rates'}]
        ]

    def test_get_historical_data(self):
        response = self.client.get('/historical_data')
        self.assertEqual(response.status_code, 200)
        expected_data = [{'id': 1, 'type': 'historical', 'data': 'Historical Data'}]
        self.assertEqual(response.json, expected_data)

    def test_get_market_trends(self):
        response = self.client.get('/market_trends')
        self.assertEqual(response.status_code, 200)
        expected_data = [{'id': 2, 'type': 'trend', 'data': 'Market Trends'}]
        self.assertEqual(response.json, expected_data)

    def test_get_lead_conversion_rates(self):
        response = self.client.get('/lead_conversion_rates')
        self.assertEqual(response.status_code, 200)
        expected_data = [{'id': 3, 'type': 'conversion_rate', 'data': 'Lead Conversion Rates'}]
        self.assertEqual(response.json, expected_data)

if __name__ == '__main__':
    unittest.main()
