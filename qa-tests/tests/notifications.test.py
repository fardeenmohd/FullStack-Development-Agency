import unittest
from app.notifications import subscribe_user, trigger_notification

class TestNotifications(unittest.TestCase):

    def test_subscribe_user(self):
        user_id = "user123"
        event_type = "new_post"
        result = subscribe_user(user_id, event_type)
        self.assertTrue(result, f"Failed to subscribe user {user_id} for event {event_type}")

    def test_trigger_notification(self):
        user_id = "user123"
        event_type = "new_post"
        message = "New post available!"
        result = trigger_notification(user_id, event_type, message)
        self.assertTrue(result, f"Failed to trigger notification for user {user_id} and event {event_type}")

if __name__ == '__main__':
    unittest.main()
