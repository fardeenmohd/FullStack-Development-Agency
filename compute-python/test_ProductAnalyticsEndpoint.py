import unittest
from fastapi.testclient import TestClient
from main import app  # Assuming the FastAPI app is defined in a file named 'main.py'
from db.session import get_db
from schemas.product_analytics import ProductAnalyticsResponse

class TestProductAnalyticsEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_product_analytics_success(self):
        # Mock the database session and product analytics retrieval
        with unittest.mock.patch('services.product_analytics_service.get_product_analytics') as mock_get_product_analytics:
            mock_get_product_analytics.return_value = ProductAnalyticsResponse(
                id=1,
                total_sales=1000,
                average_rating=4.5
            )

            response = self.client.get("/product-analytics")
            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(response.json(), dict)
            self.assertIn('id', response.json())
            self.assertIn('total_sales', response.json())
            self.assertIn('average_rating', response.json())

    def test_read_product_analytics_not_found(self):
        # Mock the database session and product analytics retrieval
        with unittest.mock.patch('services.product_analytics_service.get_product_analytics') as mock_get_product_analytics:
            mock_get_product_analytics.return_value = None

            response = self.client.get("/product-analytics")
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json(), {"detail": "Product analytics not found"})

if __name__ == '__main__':
    unittest.main()
