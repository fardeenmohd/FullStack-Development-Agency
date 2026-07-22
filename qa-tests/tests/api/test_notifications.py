import unittest
from app.api.notifications import subscribe_to_event, trigger_notification

class TestNotificationAPI(unittest.TestCase):

    def test_subscribe_to_event(self):
        user_id = "user123"
        event_type = "new_post"

        # Subscribe to an event
        result = subscribe_to_event(user_id, event_type)
        self.assertTrue(result)

        # Attempt to subscribe again (should return False as it's already subscribed)
        result = subscribe_to_event(user_id, event_type)
        self.assertFalse(result)

    def test_trigger_notification(self):
        user_id = "user123"
        event_type = "new_post"
        message = "New post available!"

        # Subscribe to the event
        subscribe_to_event(user_id, event_type)

        # Trigger a notification
        result = trigger_notification(event_type, message)
        self.assertTrue(result)

        # Verify that the user receives the notification (this is a mock implementation)
        received_notifications = get_received_notifications(user_id)  # Assume this function exists
        self.assertIn(message, received_notifications)

def get_received_notifications(user_id):
    # Mock implementation to return received notifications for a user
    return ["New post available!", "Welcome to the community!"]

if __name__ == '__main__':
    unittest.main()
