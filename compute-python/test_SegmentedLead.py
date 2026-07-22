import unittest
from fastapi.testclient import TestClient
from SegmentedLead import SegmentedLead

# Assuming the FastAPI app is defined in a file named 'main.py'
from main import app

class TestSegmentedLead(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_create_segmented_lead_valid_data(self):
        lead_data = {
            "lead_id": "12345",
            "country": "USA",
            "industry": "Technology",
            "product_interest": "AI"
        }
        response = self.client.post("/segmented_leads/", json=lead_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertIn("id", response.json())
        self.assertEqual(response.json()["country"], lead_data["country"])
        self.assertEqual(response.json()["industry"], lead_data["industry"])
        self.assertEqual(response.json()["product_interest"], lead_data["product_interest"])

    def test_create_segmented_lead_invalid_country(self):
        lead_data = {
            "lead_id": "12345",
            "country": "InvalidCountry",
            "industry": "Technology",
            "product_interest": "AI"
        }
        response = self.client.post("/segmented_leads/", json=lead_data)
        self.assertEqual(response.status_code, 400)

    def test_create_segmented_lead_missing_field(self):
        lead_data = {
            "country": "USA",
            "industry": "Technology",
            "product_interest": "AI"
        }
        response = self.client.post("/segmented_leads/", json=lead_data)
        self.assertEqual(response.status_code, 422)

    def test_get_segmented_lead_by_id(self):
        lead_data = {
            "lead_id": "12345",
            "country": "USA",
            "industry": "Technology",
            "product_interest": "AI"
        }
        response = self.client.post("/segmented_leads/", json=lead_data)
        lead_id = response.json()["id"]
        get_response = self.client.get(f"/segmented_leads/{lead_id}")
        self.assertEqual(get_response.status_code, 200)
        self.assertIsInstance(get_response.json(), dict)
        self.assertEqual(get_response.json()["id"], lead_id)

    def test_get_segmented_lead_by_invalid_id(self):
        response = self.client.get("/segmented_leads/99999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()
