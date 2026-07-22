import unittest
from lead_service import LeadService

class TestLeadService(unittest.TestCase):
    def setUp(self):
        self.lead_service = LeadService()

    def test_trigger_notification_on_new_lead(self):
        # Arrange
        new_lead = {"name": "John Doe", "email": "john.doe@example.com"}
        
        # Act
        self.lead_service.process_lead(new_lead)
        
        # Assert
        self.assertTrue(self.lead_service.notification_triggered)

if __name__ == '__main__':
    unittest.main()
