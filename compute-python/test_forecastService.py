import unittest
from fastapi.testclient import TestClient
from forecastService import app, ForecastService

class TestForecastService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.forecast_service = ForecastService('historical_data.csv')
        self.forecast_service.preprocess_data()
        self.forecast_service.train_model()

    def test_train_model(self):
        # Assuming preprocess_data and train_model are implemented correctly
        self.assertIsNotNone(self.forecast_service.model)

    def test_predict_conversion_rate(self):
        new_data = {
            'feature1': 0.5,
            'feature2': 0.3,
            # Add other features as required by your model
        }
        response = self.client.post("/predict/", json=new_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('predicted_conversion_rate', response.json())

    def test_predict_conversion_rate_with_missing_model(self):
        new_data = {
            'feature1': 0.5,
            'feature2': 0.3,
            # Add other features as required by your model
        }
        forecast_service = ForecastService('historical_data.csv')
        response = self.client.post("/predict/", json=new_data)
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
