import unittest
from unittest.mock import patch, MagicMock
from app.forecastController import ForecastController

class TestForecastController(unittest.TestCase):

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_success(self, mock_get_forecast):
        # Arrange
        forecast_controller = ForecastController()
        expected_forecast = {'temperature': 25, 'humidity': 80}
        mock_get_forecast.return_value = expected_forecast

        # Act
        result = forecast_controller.get_forecast('New York')

        # Assert
        self.assertEqual(result, expected_forecast)
        mock_get_forecast.assert_called_once_with('New York')

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_failure(self, mock_get_forecast):
        # Arrange
        forecast_controller = ForecastController()
        mock_get_forecast.side_effect = Exception('Failed to fetch forecast')

        # Act & Assert
        with self.assertRaises(Exception) as context:
            forecast_controller.get_forecast('New York')
        self.assertIn('Failed to fetch forecast', str(context.exception))

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_integration(self, mock_get_forecast):
        # Arrange
        forecast_controller = ForecastController()
        expected_forecast = {'temperature': 25, 'humidity': 80}
        mock_get_forecast.return_value = expected_forecast

        # Act
        result = forecast_controller.get_forecast('New York')

        # Assert
        self.assertEqual(result, expected_forecast)
        mock_get_forecast.assert_called_once_with('New York')

    @patch('app.forecastService.get_forecast')
    def test_get_forecast_integration_failure(self, mock_get_forecast):
        # Arrange
        forecast_controller = ForecastController()
        mock_get_forecast.side_effect = Exception('Failed to fetch forecast')

        # Act & Assert
        with self.assertRaises(Exception) as context:
            forecast_controller.get_forecast('New York')
        self.assertIn('Failed to fetch forecast', str(context.exception))

if __name__ == '__main__':
    unittest.main()
