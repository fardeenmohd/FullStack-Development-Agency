import unittest
from fastapi.testclient import TestClient
from segmentLeads import router, db_dependency

class TestSegmentLeads(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(router)

    def test_segment_leads_success(self):
        response = self.client.get("/segment_leads?criteria=test_criteria")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_segment_leads_failure(self):
        with unittest.mock.patch.object(SegmentLeadsService, 'segment_leads', side_effect=Exception("Test error")):
            response = self.client.get("/segment_leads?criteria=test_criteria")
            self.assertEqual(response.status_code, 500)
            self.assertIn("Test error", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
