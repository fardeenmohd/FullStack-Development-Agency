import unittest
from fastapi.testclient import TestClient
from forecastService import ForecastService

class TestForecastService(unittest.TestCase):
    def setUp(self):
        self.forecast_service = ForecastService('historical_data.csv')
        self.client = TestClient(forecast_service)

    def test_preprocess_data(self):
        # Assuming preprocess_data is implemented to handle missing values and encoding
        self.forecast_service.preprocess_data()
        # Add assertions to check if data preprocessing was successful

    def test_train_model(self):
        self.forecast_service.train_model()
        self.assertIsNotNone(self.forecast_service.model)

    def test_predict_conversion_rate(self):
        new_data = pd.DataFrame({'feature1': [value1], 'feature2': [value2], ...})
        predicted_conversion_rate = self.forecast_service.predict_conversion_rate(new_data)
        self.assertIsInstance(predicted_conversion_rate, np.ndarray)
        self.assertEqual(len(predicted_conversion_rate), 1)

if __name__ == "__main__":
    unittest.main()
