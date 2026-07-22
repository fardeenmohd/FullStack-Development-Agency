import unittest
from fastapi.testclient import TestClient
from leadSegmentationService import LeadSegmentationService

class TestLeadSegmentationService(unittest.TestCase):
    def setUp(self):
        self.lead_data = [
            {'id': 1, 'country': 'USA', 'industry': 'Tech', 'product_interests': ['AI', 'ML']},
            {'id': 2, 'country': 'Canada', 'industry': 'Finance', 'product_interests': ['Blockchain']},
            {'id': 3, 'country': 'USA', 'industry': 'Healthcare', 'product_interests': ['Telemedicine']}
        ]
        self.service = LeadSegmentationService(self.lead_data)

    def test_segment_leads_by_country(self):
        result = self.service.segment_leads_by_country('USA')
        expected = [1, 3]
        self.assertEqual(result, expected)

    def test_segment_leads_by_industry(self):
        result = self.service.segment_leads_by_industry('Tech')
        expected = [1]
        self.assertEqual(result, expected)

    def test_segment_leads_by_product_interest(self):
        result = self.service.segment_leads_by_product_interest('AI')
        expected = [1]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
