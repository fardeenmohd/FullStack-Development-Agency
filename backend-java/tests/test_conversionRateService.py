import unittest
from src.services.conversion_rate_service import ConversionRateService

class TestConversionRateService(unittest.TestCase):
    def setUp(self):
        self.service = ConversionRateService()

    def test_convert_currency_valid_input(self):
        result = self.service.convert_currency(100, 'USD', 'EUR')
        self.assertIsNotNone(result)
        self.assertGreater(result, 0)

    def test_convert_currency_invalid_from_currency(self):
        with self.assertRaises(ValueError):
            self.service.convert_currency(100, 'INVALID', 'EUR')

    def test_convert_currency_invalid_to_currency(self):
        with self.assertRaises(ValueError):
            self.service.convert_currency(100, 'USD', 'INVALID')

    def test_convert_currency_zero_amount(self):
        result = self.service.convert_currency(0, 'USD', 'EUR')
        self.assertEqual(result, 0)

    def test_convert_currency_negative_amount(self):
        with self.assertRaises(ValueError):
            self.service.convert_currency(-100, 'USD', 'EUR')

if __name__ == '__main__':
    unittest.main()
