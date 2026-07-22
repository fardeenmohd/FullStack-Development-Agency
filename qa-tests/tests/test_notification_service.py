import unittest
from notification_service import NotificationService

class TestNotificationService(unittest.TestCase):
    def setUp(self):
        self.service = NotificationService()

    def test_create_notification(self):
        title = "Test Title"
        content = "Test Content"
        notification_id = self.service.create_notification(title, content)
        self.assertIsNotNone(notification_id)

    def test_get_notification(self):
        title = "Test Title"
        content = "Test Content"
        notification_id = self.service.create_notification(title, content)
        retrieved_notification = self.service.get_notification(notification_id)
        self.assertEqual(retrieved_notification['title'], title)
        self.assertEqual(retrieved_notification['content'], content)

    def test_update_notification(self):
        title = "Test Title"
        content = "Test Content"
        new_content = "Updated Content"
        notification_id = self.service.create_notification(title, content)
        self.service.update_notification(notification_id, new_content)
        updated_notification = self.service.get_notification(notification_id)
        self.assertEqual(updated_notification['content'], new_content)

    def test_handle_lead_status_change(self):
        lead_id = 123
        old_status = "Pending"
        new_status = "Converted"
        notification_type = "Lead Status Change"

        # Create a notification for the lead status change
        notification_id = self.service.create_notification(notification_type, f"Lead {lead_id} status changed from {old_status} to {new_status}")

        # Retrieve and verify the notification
        retrieved_notification = self.service.get_notification(notification_id)
        self.assertEqual(retrieved_notification['title'], notification_type)
        self.assertIn(f"Lead {lead_id} status changed from {old_status} to {new_status}", retrieved_notification['content'])

    def test_handle_lead_status_change_with_custom_message(self):
        lead_id = 456
        old_status = "Pending"
        new_status = "Rejected"
        custom_message = "Please review the lead details."
        notification_type = "Lead Status Change"

        # Create a notification for the lead status change with a custom message
        notification_id = self.service.create_notification(notification_type, f"Lead {lead_id} status changed from {old_status} to {new_status}. {custom_message}")

        # Retrieve and verify the notification
        retrieved_notification = self.service.get_notification(notification_id)
        self.assertEqual(retrieved_notification['title'], notification_type)
        self.assertIn(f"Lead {lead_id} status changed from {old_status} to {new_status}", retrieved_notification['content'])
        self.assertIn(custom_message, retrieved_notification['content'])

if __name__ == '__main__':
    unittest.main()
