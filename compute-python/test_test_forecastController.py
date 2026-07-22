import unittest
from fastapi.testclient import TestClient
from app.forecastController import ForecastController

class TestForecastController(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(ForecastController())

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_success(self, mock_get_forecast):
        # Arrange
        expected_forecast = {'temperature': 25, 'humidity': 80}
        mock_get_forecast.return_value = expected_forecast

        # Act
        response = self.client.get('/forecast?city=New%20York')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_forecast)
        mock_get_forecast.assert_called_once_with('New York')

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_failure(self, mock_get_forecast):
        # Arrange
        mock_get_forecast.side_effect = Exception('Failed to fetch forecast')

        # Act & Assert
        response = self.client.get('/forecast?city=New%20York')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Failed to fetch forecast', response.text)

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_integration(self, mock_get_forecast):
        # Arrange
        expected_forecast = {'temperature': 25, 'humidity': 80}
        mock_get_forecast.return_value = expected_forecast

        # Act
        response = self.client.get('/forecast?city=New%20York')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_forecast)
        mock_get_forecast.assert_called_once_with('New York')

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_integration_failure(self, mock_get_forecast):
        # Arrange
        mock_get_forecast.side_effect = Exception('Failed to fetch forecast')

        # Act & Assert
        response = self.client.get('/forecast?city=New%20York')
        self.assertEqual(response.status_code, 500)
        self.assertIn('Failed to fetch forecast', response.text)

if __name__ == '__main__':
    unittest.main()
