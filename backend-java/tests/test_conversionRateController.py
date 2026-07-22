import unittest
from unittest.mock import patch, MagicMock
from app.controllers.conversion_rate_controller import ConversionRateController

class TestConversionRateController(unittest.TestCase):

    @patch('app.services.currency_service.get_conversion_rate')
    def test_get_conversion_rate_success(self, mock_get_conversion_rate):
        # Arrange
        controller = ConversionRateController()
        mock_get_conversion_rate.return_value = 1.20
        from_currency = 'USD'
        to_currency = 'EUR'

        # Act
        result = controller.get_conversion_rate(from_currency, to_currency)

        # Assert
        self.assertEqual(result, 1.20)
        mock_get_conversion_rate.assert_called_once_with(from_currency, to_currency)

    @patch('app.services.currency_service.get_conversion_rate')
    def test_get_conversion_rate_failure(self, mock_get_conversion_rate):
        # Arrange
        controller = ConversionRateController()
        mock_get_conversion_rate.side_effect = Exception("Failed to fetch conversion rate")
        from_currency = 'USD'
        to_currency = 'EUR'

        # Act & Assert
        with self.assertRaises(Exception) as context:
            controller.get_conversion_rate(from_currency, to_currency)
        self.assertIn("Failed to fetch conversion rate", str(context.exception))

if __name__ == '__main__':
    unittest.main()
