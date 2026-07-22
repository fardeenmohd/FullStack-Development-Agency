import unittest
from forecast_service import ForecastService

class TestForecastService(unittest.TestCase):
    def setUp(self):
        self.forecast_service = ForecastService()

    def test_calculate_lead_conversion_rate(self):
        # Mock historical data and current market trends
        historical_data = {'total_leads': 100, 'converted_leads': 20}
        current_trends = {'conversion_rate_increase': 5}

        # Calculate lead conversion rate
        conversion_rate = self.forecast_service.calculate_lead_conversion_rate(historical_data, current_trends)

        # Assert the calculated conversion rate is as expected
        expected_conversion_rate = (historical_data['converted_leads'] / historical_data['total_leads']) * (1 + current_trends['conversion_rate_increase'] / 100)
        self.assertAlmostEqual(conversion_rate, expected_conversion_rate, places=2)

    def test_calculate_lead_conversion_rate_with_zero_total_leads(self):
        # Mock historical data and current market trends
        historical_data = {'total_leads': 0, 'converted_leads': 20}
        current_trends = {'conversion_rate_increase': 5}

        # Calculate lead conversion rate
        conversion_rate = self.forecast_service.calculate_lead_conversion_rate(historical_data, current_trends)

        # Assert the calculated conversion rate is as expected (should be 0)
        self.assertEqual(conversion_rate, 0)

    def test_calculate_lead_conversion_rate_with_negative_converted_leads(self):
        # Mock historical data and current market trends
        historical_data = {'total_leads': 100, 'converted_leads': -20}
        current_trends = {'conversion_rate_increase': 5}

        # Calculate lead conversion rate
        conversion_rate = self.forecast_service.calculate_lead_conversion_rate(historical_data, current_trends)

        # Assert the calculated conversion rate is as expected (should be 0)
        self.assertEqual(conversion_rate, 0)

    def test_calculate_lead_conversion_rate_with_zero_conversion_rate_increase(self):
        # Mock historical data and current market trends
        historical_data = {'total_leads': 100, 'converted_leads': 20}
        current_trends = {'conversion_rate_increase': 0}

        # Calculate lead conversion rate
        conversion_rate = self.forecast_service.calculate_lead_conversion_rate(historical_data, current_trends)

        # Assert the calculated conversion rate is as expected
        expected_conversion_rate = historical_data['converted_leads'] / historical_data['total_leads']
        self.assertAlmostEqual(conversion_rate, expected_conversion_rate, places=2)

if __name__ == '__main__':
    unittest.main()
